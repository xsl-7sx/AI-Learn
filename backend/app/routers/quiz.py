import asyncio

from fastapi import APIRouter, HTTPException

from app.chains.quiz_generation import QuizGenerationError, generate_quiz
from app.chains.report_generation import generate_report
from app.config import settings
from app.schemas.quiz import (
  GenerateQuizRequest,
  GenerateQuizResponse,
  QuizReportRequest,
  QuizReportResponse,
)

router = APIRouter(prefix="/api/v1/quiz", tags=["quiz"])


@router.post("/generate", response_model=GenerateQuizResponse)
async def create_quiz(payload: GenerateQuizRequest) -> GenerateQuizResponse:
  try:
    return await asyncio.wait_for(
      generate_quiz(payload.topic),
      timeout=settings.request_total_timeout,
    )
  except asyncio.TimeoutError as exc:
    raise HTTPException(status_code=504, detail="request timeout") from exc
  except QuizGenerationError as exc:
    raise HTTPException(status_code=502, detail=str(exc)) from exc


@router.post("/report", response_model=QuizReportResponse)
async def create_report(payload: QuizReportRequest) -> QuizReportResponse:
  try:
    return await asyncio.wait_for(
      generate_report(payload),
      timeout=30,
    )
  except asyncio.TimeoutError as exc:
    raise HTTPException(status_code=504, detail="request timeout") from exc
