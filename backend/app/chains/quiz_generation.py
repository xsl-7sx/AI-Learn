from __future__ import annotations

import json
import re
from datetime import datetime
from uuid import uuid4

from fastapi import HTTPException
from langchain_core.output_parsers import PydanticOutputParser
from langchain_core.prompts import ChatPromptTemplate

from app.chains.llm import get_llm
from app.chains.mock_data import build_mock_quiz
from app.config import settings
from app.prompts.quiz_generation import QUIZ_GENERATION_SYSTEM, QUIZ_GENERATION_USER
from app.schemas.quiz import GenerateQuizResponse


class QuizGenerationError(Exception):
  pass


def _strip_code_fence(text: str) -> str:
  cleaned = text.strip()
  if cleaned.startswith("```"):
    cleaned = re.sub(r"^```(?:json)?\s*", "", cleaned)
    cleaned = re.sub(r"\s*```$", "", cleaned)
  return cleaned.strip()


def _parse_quiz_payload(raw_text: str) -> GenerateQuizResponse:
  parser = PydanticOutputParser(pydantic_object=GenerateQuizResponse)
  cleaned = _strip_code_fence(raw_text)

  try:
    return parser.parse(cleaned)
  except Exception as first_error:
    llm = get_llm()
    fix_prompt = (
      "下面是一段应输出为 JSON 的文本，但解析失败。"
      f"错误：{first_error}\n"
      f"请只输出修复后的纯 JSON，符合格式：{parser.get_format_instructions()}\n"
      f"原文：\n{cleaned}"
    )
    try:
      fixed = llm.invoke(fix_prompt)
      content = fixed.content if isinstance(fixed.content, str) else json.dumps(fixed.content)
      return parser.parse(_strip_code_fence(content))
    except Exception as exc:
      raise QuizGenerationError("failed to parse quiz json") from exc


async def generate_quiz(topic: str) -> GenerateQuizResponse:
  if settings.mock_llm or not settings.resolved_api_key:
    return build_mock_quiz(topic)

  parser = PydanticOutputParser(pydantic_object=GenerateQuizResponse)
  prompt = ChatPromptTemplate.from_messages(
    [
      ("system", QUIZ_GENERATION_SYSTEM),
      ("human", QUIZ_GENERATION_USER),
    ]
  )
  chain = prompt | get_llm()
  result = await chain.ainvoke(
    {
      "topic": topic,
      "format_instructions": parser.get_format_instructions(),
    }
  )
  content = result.content if isinstance(result.content, str) else json.dumps(result.content)
  parsed = _parse_quiz_payload(content)
  return parsed.model_copy(
    update={
      "quiz_id": f"q_{datetime.now().strftime('%Y%m%d')}_{uuid4().hex[:8]}",
      "topic": topic,
    }
  )


def to_http_exception(exc: QuizGenerationError) -> HTTPException:
  return HTTPException(status_code=502, detail=str(exc))
