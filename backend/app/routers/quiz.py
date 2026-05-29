import asyncio
import logging

from fastapi import APIRouter, BackgroundTasks, HTTPException

from app.chains.quiz_generation import QuizGenerationError, generate_quiz
from app.chains.report_generation import generate_report
from app.config import settings
from app.jobs.quiz_jobs import quiz_job_store
from app.schemas.quiz import (
  GenerateQuizJobResponse,
  GenerateQuizRequest,
  QuizJobStatusResponse,
  QuizReportRequest,
  QuizReportResponse,
)

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/v1/quiz", tags=["quiz"])


async def _run_quiz_job(job_id: str, topic: str) -> None:
  await quiz_job_store.mark_running(job_id)
  try:
    result = await asyncio.wait_for(
      generate_quiz(topic),
      timeout=settings.request_total_timeout,
    )
    await quiz_job_store.mark_completed(job_id, result)
  except asyncio.TimeoutError:
    await quiz_job_store.mark_failed(job_id, "request timeout")
  except QuizGenerationError as exc:
    await quiz_job_store.mark_failed(job_id, str(exc))
  except Exception:
    logger.exception("quiz job %s failed", job_id)
    await quiz_job_store.mark_failed(job_id, "AI 生成失败，请重试")


@router.post("/generate", response_model=GenerateQuizJobResponse, status_code=202)
async def create_quiz(
  payload: GenerateQuizRequest,
  background_tasks: BackgroundTasks,
) -> GenerateQuizJobResponse:
  job = await quiz_job_store.create(payload.topic)
  background_tasks.add_task(_run_quiz_job, job.job_id, payload.topic)
  return GenerateQuizJobResponse(job_id=job.job_id)


@router.get("/jobs/{job_id}", response_model=QuizJobStatusResponse)
async def get_quiz_job(job_id: str) -> QuizJobStatusResponse:
  job = await quiz_job_store.get(job_id)
  if job is None:
    raise HTTPException(status_code=404, detail="job not found")

  return QuizJobStatusResponse(
    job_id=job.job_id,
    status=job.status,
    result=job.result,
    error=job.error,
  )


@router.post("/report", response_model=QuizReportResponse)
async def create_report(payload: QuizReportRequest) -> QuizReportResponse:
  try:
    return await asyncio.wait_for(
      generate_report(payload),
      timeout=30,
    )
  except asyncio.TimeoutError as exc:
    raise HTTPException(status_code=504, detail="request timeout") from exc
