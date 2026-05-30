from __future__ import annotations

import json
import re

from langchain_core.prompts import ChatPromptTemplate

from app.chains.llm import get_llm
from app.chains.mock_data import build_mock_report
from app.config import settings
from app.prompts.report_generation import REPORT_GENERATION_SYSTEM, REPORT_GENERATION_USER
from app.schemas.quiz import QuizReportRequest, QuizReportResponse

_TRAILING_EMPTY_PARENS = re.compile(r"[（(]\s*[）)]\s*$")
_JSON_FENCE_RE = re.compile(r"^```(?:json)?\s*|\s*```$", re.IGNORECASE | re.MULTILINE)


def _sanitize_question_stem(stem: str) -> str:
  return _TRAILING_EMPTY_PARENS.sub("", stem).rstrip()


def _sanitize_text_list(items: list[object]) -> list[str]:
  cleaned: list[str] = []
  for item in items:
    text = _sanitize_question_stem(str(item).strip())
    if text:
      cleaned.append(text)
  return cleaned


def _sanitize_structured_payload(data: object) -> object:
  if not isinstance(data, dict):
    return data

  root = data.get("学习复盘报告", data)
  if not isinstance(root, dict):
    return data

  if isinstance(root.get("整体表现"), str):
    root["整体表现"] = _sanitize_question_stem(root["整体表现"])

  for key in ("核心知识点回顾", "易错题分析", "复习建议"):
    value = root.get(key)
    if isinstance(value, list):
      root[key] = _sanitize_text_list(value)

  if "学习复盘报告" in data:
    data["学习复盘报告"] = root
  return data


def _extract_first_json_object(text: str) -> str:
  candidate = _JSON_FENCE_RE.sub("", text).strip()
  try:
    json.loads(candidate)
    return candidate
  except json.JSONDecodeError:
    pass

  start = candidate.find("{")
  if start == -1:
    return candidate

  depth = 0
  in_string = False
  escaped = False
  for index in range(start, len(candidate)):
    ch = candidate[index]
    if in_string:
      if escaped:
        escaped = False
      elif ch == "\\":
        escaped = True
      elif ch == '"':
        in_string = False
      continue
    if ch == '"':
      in_string = True
      continue
    if ch == "{":
      depth += 1
    elif ch == "}":
      depth -= 1
      if depth == 0:
        return candidate[start : index + 1]
  return candidate[start:]


def _sanitize_report_text(report: str) -> str:
  raw = report.strip()
  if not raw:
    return raw

  json_text = _extract_first_json_object(raw)
  if json_text.startswith("{"):
    try:
      payload = json.loads(json_text)
      payload = _sanitize_structured_payload(payload)
      return json.dumps(payload, ensure_ascii=False)
    except json.JSONDecodeError:
      pass

  return "\n".join(_sanitize_question_stem(line).rstrip() for line in report.splitlines())


def _build_answers_summary(payload: QuizReportRequest) -> str:
  question_map = {question.id: question for question in payload.questions}
  lines: list[str] = []
  for answer in payload.answers:
    question = question_map.get(answer.question_id)
    raw_stem = question.stem if question else answer.question_id
    stem = _sanitize_question_stem(raw_stem)
    status = "正确" if answer.correct else "错误"
    lines.append(f"- [{status}] {stem} | 你的选择: {answer.selected}")
  return "\n".join(lines)


async def generate_report(payload: QuizReportRequest) -> QuizReportResponse:
  total = len(payload.questions)
  score = sum(1 for answer in payload.answers if answer.correct)
  correct_rate = round(score / total, 2) if total else 0.0

  if settings.use_mock_llm:
    question_map = {question.id: question for question in payload.questions}
    wrong_stems = [
      _sanitize_question_stem(question_map[a.question_id].stem)
      for a in payload.answers
      if not a.correct and a.question_id in question_map
    ]
    return QuizReportResponse(
      score=score,
      total=total,
      correct_rate=correct_rate,
      report=_sanitize_report_text(
        build_mock_report(
          topic=payload.topic,
          score=score,
          total=total,
          wrong_stems=wrong_stems,
        )
      ),
    )
  if not settings.resolved_api_key:
    raise ValueError("LLM API key not configured")

  prompt = ChatPromptTemplate.from_messages(
    [
      ("system", REPORT_GENERATION_SYSTEM),
      ("human", REPORT_GENERATION_USER),
    ]
  )
  chain = prompt | get_llm()
  result = await chain.ainvoke(
    {
      "topic": payload.topic,
      "answers_summary": _build_answers_summary(payload),
    }
  )
  report_text = result.content if isinstance(result.content, str) else str(result.content)
  return QuizReportResponse(
    score=score,
    total=total,
    correct_rate=correct_rate,
    report=_sanitize_report_text(report_text.strip()),
  )
