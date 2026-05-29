import asyncio
import logging
from datetime import datetime
from uuid import uuid4

from fastapi import APIRouter, BackgroundTasks, HTTPException

from app.chains.quiz_generation import QuizGenerationError
from app.chains.quiz_stream_generation import stream_generate_quiz
from app.chains.report_generation import generate_report
from app.config import settings
from app.jobs.quiz_jobs import quiz_job_store
from app.schemas.quiz import (
  GenerateQuizJobResponse,
  GenerateQuizRequest,
  QuizJobStatusResponse,
  QuizReportRequest,
  QuizReportResponse,
  Question,
)

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/v1/quiz", tags=["quiz"])


def _job_to_response(job) -> QuizJobStatusResponse:
  return QuizJobStatusResponse(
    job_id=job.job_id,
    status=job.status,
    quiz_id=job.quiz_id,
    topic=job.topic,
    questions=job.questions,
    total_expected=job.expected_total,
    ready=len(job.questions) > 0,
    stream_preview=job.stream_preview,
    result=job.result,
    error=job.error,
  )


async def _run_quiz_job(job_id: str, topic: str) -> None:
  quiz_id = f"q_{datetime.now().strftime('%Y%m%d')}_{uuid4().hex[:8]}"
  await quiz_job_store.mark_running(job_id, quiz_id=quiz_id)

  async def on_preview(preview: str) -> None:
    await quiz_job_store.set_preview(job_id, preview)

  async def on_question(question: Question) -> None:
    await quiz_job_store.append_question(job_id, question)

  try:
    result = await asyncio.wait_for(
      stream_generate_quiz(topic, on_question=on_question, on_preview=on_preview),
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
  return _job_to_response(job)


@router.post("/report", response_model=QuizReportResponse)
async def create_report(payload: QuizReportRequest) -> QuizReportResponse:
  try:
    return await asyncio.wait_for(
      generate_report(payload),
      timeout=30,
    )
  except asyncio.TimeoutError as exc:
    raise HTTPException(status_code=504, detail="request timeout") from exc
