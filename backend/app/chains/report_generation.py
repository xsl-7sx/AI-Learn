from __future__ import annotations

from langchain_core.prompts import ChatPromptTemplate

from app.chains.llm import get_llm
from app.chains.mock_data import MOCK_REPORT
from app.config import settings
from app.prompts.report_generation import REPORT_GENERATION_SYSTEM, REPORT_GENERATION_USER
from app.schemas.quiz import QuizReportRequest, QuizReportResponse


def _build_answers_summary(payload: QuizReportRequest) -> str:
  question_map = {question.id: question for question in payload.questions}
  lines: list[str] = []
  for answer in payload.answers:
    question = question_map.get(answer.question_id)
    stem = question.stem if question else answer.question_id
    status = "正确" if answer.correct else "错误"
    lines.append(f"- [{status}] {stem} | 你的选择: {answer.selected}")
  return "\n".join(lines)


async def generate_report(payload: QuizReportRequest) -> QuizReportResponse:
  total = len(payload.questions)
  score = sum(1 for answer in payload.answers if answer.correct)
  correct_rate = round(score / total, 2) if total else 0.0

  if settings.mock_llm:
    return QuizReportResponse(
      score=score,
      total=total,
      correct_rate=correct_rate,
      report=MOCK_REPORT,
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
    report=report_text.strip(),
  )
