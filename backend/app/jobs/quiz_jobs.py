from __future__ import annotations

import asyncio
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import Literal
from uuid import uuid4

from app.schemas.quiz import GenerateQuizResponse, Question

JobStatus = Literal["pending", "running", "completed", "failed"]
EXPECTED_QUESTION_COUNT = 10


@dataclass
class QuizJob:
  job_id: str
  topic: str
  status: JobStatus = "pending"
  quiz_id: str | None = None
  questions: list[Question] = field(default_factory=list)
  stream_preview: str = ""
  expected_total: int = EXPECTED_QUESTION_COUNT
  result: GenerateQuizResponse | None = None
  error: str | None = None
  created_at: datetime = field(default_factory=datetime.now)
  updated_at: datetime = field(default_factory=datetime.now)


class QuizJobStore:
  def __init__(self, *, ttl_seconds: int = 3600, max_jobs: int = 200) -> None:
    self._jobs: dict[str, QuizJob] = {}
    self._lock = asyncio.Lock()
    self._ttl = timedelta(seconds=ttl_seconds)
    self._max_jobs = max_jobs

  def _new_job_id(self) -> str:
    return f"job_{datetime.now().strftime('%Y%m%d')}_{uuid4().hex[:10]}"

  async def _prune(self) -> None:
    if len(self._jobs) <= self._max_jobs:
      return
    now = datetime.now()
    expired = [
      job_id
      for job_id, job in self._jobs.items()
      if now - job.created_at > self._ttl
    ]
    for job_id in expired:
      self._jobs.pop(job_id, None)

  async def create(self, topic: str) -> QuizJob:
    async with self._lock:
      await self._prune()
      job = QuizJob(job_id=self._new_job_id(), topic=topic)
      self._jobs[job.job_id] = job
      return job

  async def get(self, job_id: str) -> QuizJob | None:
    async with self._lock:
      job = self._jobs.get(job_id)
      if job is None:
        return None
      if datetime.now() - job.created_at > self._ttl:
        self._jobs.pop(job_id, None)
        return None
      return job

  async def mark_running(self, job_id: str, *, quiz_id: str) -> QuizJob | None:
    async with self._lock:
      job = self._jobs.get(job_id)
      if job is None:
        return None
      job.status = "running"
      job.quiz_id = quiz_id
      job.updated_at = datetime.now()
      return job

  async def set_preview(self, job_id: str, preview: str) -> QuizJob | None:
    async with self._lock:
      job = self._jobs.get(job_id)
      if job is None:
        return None
      job.stream_preview = preview
      job.updated_at = datetime.now()
      return job

  async def append_question(self, job_id: str, question: Question) -> QuizJob | None:
    async with self._lock:
      job = self._jobs.get(job_id)
      if job is None:
        return None
      if any(existing.id == question.id for existing in job.questions):
        return job
      job.questions.append(question)
      job.updated_at = datetime.now()
      return job

  async def mark_completed(self, job_id: str, result: GenerateQuizResponse) -> QuizJob | None:
    async with self._lock:
      job = self._jobs.get(job_id)
      if job is None:
        return None
      job.status = "completed"
      job.quiz_id = result.quiz_id
      job.questions = result.questions
      job.result = result
      job.error = None
      job.updated_at = datetime.now()
      return job

  async def mark_failed(self, job_id: str, error: str) -> QuizJob | None:
    async with self._lock:
      job = self._jobs.get(job_id)
      if job is None:
        return None
      job.status = "failed"
      job.error = error
      job.updated_at = datetime.now()
      return job


quiz_job_store = QuizJobStore()
