from __future__ import annotations

import asyncio
import json
import re
from collections.abc import Awaitable, Callable
from datetime import datetime
from uuid import uuid4

from langchain_core.output_parsers import PydanticOutputParser
from langchain_core.prompts import ChatPromptTemplate

from app.chains.llm import get_llm
from app.chains.mock_data import build_mock_quiz
from app.chains.quiz_generation import QuizGenerationError
from app.config import settings
from app.prompts.quiz_stream_generation import (
  QUIZ_STREAM_SYSTEM,
  QUIZ_STREAM_USER,
  QUIZ_TOPUP_SYSTEM,
  QUIZ_TOPUP_USER,
)
from app.schemas.quiz import GenerateQuizResponse, Question

EXPECTED_QUESTION_COUNT = 10
MAX_TOPUP_ATTEMPTS = 2
OnQuestion = Callable[[Question], Awaitable[None]]
OnPreview = Callable[[str], Awaitable[None]]

class QuestionStreamParser:
  def __init__(self) -> None:
    self._buffer = ""
    self._seen_ids: set[str] = set()

  def feed(self, chunk: str) -> list[Question]:
    self._buffer += chunk
    found: list[Question] = []

    while "\n" in self._buffer:
      line, self._buffer = self._buffer.split("\n", 1)
      question = self._parse_line(line)
      if question is not None:
        found.append(question)

    found.extend(self._extract_inline_objects())
    return found

  def flush(self) -> list[Question]:
    remaining = self._buffer.strip()
    self._buffer = ""
    if not remaining:
      return []
    question = self._parse_line(remaining)
    return [question] if question is not None else []

  def _parse_line(self, line: str) -> Question | None:
    cleaned = line.strip().rstrip(",")
    if not cleaned or cleaned in {"[", "]"}:
      return None
    return self._validate_question_text(cleaned)

  def _extract_inline_objects(self) -> list[Question]:
    found: list[Question] = []
    decoder = json.JSONDecoder()
    raw = self._buffer.lstrip()
    if raw.startswith("["):
      raw = raw[1:].lstrip()
      self._buffer = raw

    idx = 0
    while idx < len(raw):
      part = raw[idx:].lstrip()
      if not part or part.startswith("]"):
        break
      if part[0] == ",":
        idx += 1
        continue
      if part[0] != "{":
        break
      try:
        obj, end = decoder.raw_decode(part)
        question = Question.model_validate(obj)
        if question.id not in self._seen_ids:
          self._seen_ids.add(question.id)
          found.append(question)
        idx += len(raw[idx:]) - len(part) + end
      except (json.JSONDecodeError, ValueError):
        break

    self._buffer = raw[idx:]
    return found

  def _validate_question_text(self, text: str) -> Question | None:
    if not text.startswith("{"):
      return None
    try:
      question = Question.model_validate(json.loads(text))
    except (json.JSONDecodeError, ValueError):
      return None
    if question.id in self._seen_ids:
      return None
    self._seen_ids.add(question.id)
    return question


def _chunk_text(chunk: object) -> str:
  content = getattr(chunk, "content", chunk)
  if isinstance(content, str):
    return content
  if isinstance(content, list):
    parts: list[str] = []
    for item in content:
      if isinstance(item, str):
        parts.append(item)
      elif isinstance(item, dict) and item.get("type") == "text":
        parts.append(str(item.get("text", "")))
    return "".join(parts)
  return ""


def _preview_tail(text: str, *, limit: int = 120) -> str:
  compact = re.sub(r"\s+", " ", text).strip()
  if len(compact) <= limit:
    return compact
  return f"…{compact[-limit:]}"


def _question_sort_key(question: Question) -> int:
  match = re.fullmatch(r"q(\d+)", question.id)
  return int(match.group(1)) if match else 999


def _missing_question_ids(collected: list[Question]) -> list[str]:
  existing = {question.id for question in collected}
  return [f"q{index}" for index in range(1, EXPECTED_QUESTION_COUNT + 1) if f"q{index}" not in existing]


def _sort_questions_by_id(questions: list[Question]) -> list[Question]:
  return sorted(questions, key=_question_sort_key)


def _existing_summary(collected: list[Question]) -> str:
  if not collected:
    return "（无）"
  lines = []
  for question in sorted(collected, key=_question_sort_key):
    stem = re.sub(r"\s+", " ", question.stem).strip()
    if len(stem) > 48:
      stem = f"{stem[:48]}…"
    lines.append(f"- {question.id}: {stem}")
  return "\n".join(lines)


def _salvage_questions_from_text(text: str, seen_ids: set[str]) -> list[Question]:
  found: list[Question] = []
  decoder = json.JSONDecoder()
  idx = 0
  while idx < len(text):
    start = text.find("{", idx)
    if start == -1:
      break
    try:
      obj, end = decoder.raw_decode(text[start:])
      question = Question.model_validate(obj)
    except (json.JSONDecodeError, ValueError):
      idx = start + 1
      continue
    if question.id in seen_ids:
      idx = start + end
      continue
    found.append(question)
    idx = start + end
  return found


async def _consume_question_stream(
  topic: str,
  *,
  system_prompt: str,
  user_prompt: str,
  seen_ids: set[str],
  on_question: OnQuestion,
  on_preview: OnPreview,
) -> list[Question]:
  parser = PydanticOutputParser(pydantic_object=Question)
  prompt = ChatPromptTemplate.from_messages(
    [
      ("system", system_prompt),
      ("human", user_prompt),
    ]
  )
  chain = prompt | get_llm(json_mode=False)
  stream_parser = QuestionStreamParser()
  stream_parser._seen_ids = set(seen_ids)
  preview_text = ""
  found: list[Question] = []

  async def emit_question(question: Question) -> None:
    if question.id in seen_ids:
      return
    found.append(question)
    await on_question(question)

  async for chunk in chain.astream(
    {
      "topic": topic,
      "format_instructions": parser.get_format_instructions(),
    }
  ):
    text = _chunk_text(chunk)
    if not text:
      continue
    preview_text += text
    await on_preview(_preview_tail(preview_text))
    for question in stream_parser.feed(text):
      await emit_question(question)

  for question in stream_parser.flush():
    await emit_question(question)

  for question in _salvage_questions_from_text(preview_text, seen_ids):
    await emit_question(question)

  return found


async def _stream_topup_questions(
  topic: str,
  collected: list[Question],
  missing_ids: list[str],
  *,
  on_question: OnQuestion,
  on_preview: OnPreview,
) -> list[Question]:
  if not missing_ids:
    return []

  seen_ids = {question.id for question in collected}
  await on_preview(f"正在补全缺失题目（{len(missing_ids)} 题）…")
  return await _consume_question_stream(
    topic,
    system_prompt=QUIZ_TOPUP_SYSTEM,
    user_prompt=QUIZ_TOPUP_USER.format(
      topic=topic,
      existing_summary=_existing_summary(collected),
      missing_ids=", ".join(missing_ids),
    ),
    seen_ids=seen_ids,
    on_question=on_question,
    on_preview=on_preview,
  )


async def stream_generate_quiz(
  topic: str,
  *,
  quiz_id: str | None = None,
  on_question: OnQuestion,
  on_preview: OnPreview,
) -> GenerateQuizResponse:
  resolved_quiz_id = quiz_id or f"q_{datetime.now().strftime('%Y%m%d')}_{uuid4().hex[:8]}"

  if settings.use_mock_llm:
    return await _stream_mock_quiz(topic, resolved_quiz_id, on_question=on_question, on_preview=on_preview)

  if not settings.resolved_api_key:
    raise QuizGenerationError("LLM API key not configured")

  collected: list[Question] = []
  seen_ids: set[str] = set()

  async def collect_question(question: Question) -> None:
    if question.id in seen_ids:
      return
    seen_ids.add(question.id)
    collected.append(question)
    await on_question(question)

  await on_preview("正在生成题目…")
  await _consume_question_stream(
    topic,
    system_prompt=QUIZ_STREAM_SYSTEM,
    user_prompt=QUIZ_STREAM_USER.format(topic=topic),
    seen_ids=seen_ids,
    on_question=collect_question,
    on_preview=on_preview,
  )

  topup_attempts = 0
  while len(collected) < EXPECTED_QUESTION_COUNT and topup_attempts < MAX_TOPUP_ATTEMPTS:
    missing_ids = _missing_question_ids(collected)
    if not missing_ids:
      break
    topup_attempts += 1
    await _stream_topup_questions(
      topic,
      collected,
      missing_ids,
      on_question=collect_question,
      on_preview=on_preview,
    )
    if len(collected) >= EXPECTED_QUESTION_COUNT:
      break

  ordered = _sort_questions_by_id(collected)
  if len(ordered) != EXPECTED_QUESTION_COUNT:
    raise QuizGenerationError(f"expected {EXPECTED_QUESTION_COUNT} questions, got {len(ordered)}")

  return GenerateQuizResponse(quiz_id=resolved_quiz_id, topic=topic, questions=ordered)


async def _stream_mock_quiz(
  topic: str,
  quiz_id: str,
  *,
  on_question: OnQuestion,
  on_preview: OnPreview,
) -> GenerateQuizResponse:
  quiz = build_mock_quiz(topic)
  collected: list[Question] = []

  for index, question in enumerate(quiz.questions):
    await on_preview(f"正在生成第 {index + 1}/{EXPECTED_QUESTION_COUNT} 题…")
    await on_question(question)
    collected.append(question)
    if index < len(quiz.questions) - 1:
      await asyncio.sleep(0.03)

  return GenerateQuizResponse(quiz_id=quiz_id, topic=topic, questions=collected)
