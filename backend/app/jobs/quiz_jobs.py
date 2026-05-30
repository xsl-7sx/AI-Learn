from __future__ import annotations

import asyncio
import json
import time
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from pathlib import Path
from typing import Literal
from uuid import uuid4

from app.schemas.quiz import GenerateQuizResponse, Question

JobStatus = Literal["pending", "running", "completed", "failed"]
EXPECTED_QUESTION_COUNT = 10
JOB_DATA_DIR = Path(__file__).resolve().parents[2] / "data" / "quiz_jobs"


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


PREVIEW_PERSIST_INTERVAL_S = 0.4


class QuizJobStore:
  def __init__(self, *, ttl_seconds: int = 3600, max_jobs: int = 200) -> None:
    self._jobs: dict[str, QuizJob] = {}
    self._lock = asyncio.Lock()
    self._ttl = timedelta(seconds=ttl_seconds)
    self._max_jobs = max_jobs
    self._preview_last_persist: dict[str, float] = {}
    self._preview_persist_count = 0
    self._preview_skip_count = 0

  def _new_job_id(self) -> str:
    return f"job_{datetime.now().strftime('%Y%m%d')}_{uuid4().hex[:10]}"

  def _job_path(self, job_id: str) -> Path:
    return JOB_DATA_DIR / f"{job_id}.json"

  def _serialize_job(self, job: QuizJob) -> dict:
    return {
      "job_id": job.job_id,
      "topic": job.topic,
      "status": job.status,
      "quiz_id": job.quiz_id,
      "questions": [question.model_dump() for question in job.questions],
      "stream_preview": job.stream_preview,
      "expected_total": job.expected_total,
      "result": job.result.model_dump() if job.result else None,
      "error": job.error,
      "created_at": job.created_at.isoformat(),
      "updated_at": job.updated_at.isoformat(),
    }

  def _deserialize_job(self, data: dict) -> QuizJob:
    questions = [Question.model_validate(item) for item in data.get("questions", [])]
    result_data = data.get("result")
    result = GenerateQuizResponse.model_validate(result_data) if result_data else None
    return QuizJob(
      job_id=data["job_id"],
      topic=data["topic"],
      status=data["status"],
      quiz_id=data.get("quiz_id"),
      questions=questions,
      stream_preview=data.get("stream_preview", ""),
      expected_total=data.get("expected_total", EXPECTED_QUESTION_COUNT),
      result=result,
      error=data.get("error"),
      created_at=datetime.fromisoformat(data["created_at"]),
      updated_at=datetime.fromisoformat(data["updated_at"]),
    )

  def _persist(self, job: QuizJob) -> None:
    JOB_DATA_DIR.mkdir(parents=True, exist_ok=True)
    self._job_path(job.job_id).write_text(
      json.dumps(self._serialize_job(job), ensure_ascii=False),
      encoding="utf-8",
    )

  def _load_from_disk(self, job_id: str) -> QuizJob | None:
    path = self._job_path(job_id)
    if not path.exists():
      return None
    try:
      data = json.loads(path.read_text(encoding="utf-8"))
      return self._deserialize_job(data)
    except (json.JSONDecodeError, KeyError, ValueError, TypeError):
      return None

  def _delete_from_disk(self, job_id: str) -> None:
    path = self._job_path(job_id)
    if path.exists():
      path.unlink()

  def _get_locked(self, job_id: str) -> QuizJob | None:
    job = self._jobs.get(job_id)
    if job is not None:
      return job
    job = self._load_from_disk(job_id)
    if job is not None:
      self._jobs[job_id] = job
    return job

  async def _prune(self) -> None:
    now = datetime.now()
    expired = [
      job_id
      for job_id, job in self._jobs.items()
      if now - job.created_at > self._ttl
    ]
    for job_id in expired:
      self._jobs.pop(job_id, None)
      self._delete_from_disk(job_id)

    if len(self._jobs) <= self._max_jobs:
      return

    overflow = len(self._jobs) - self._max_jobs
    oldest = sorted(self._jobs.values(), key=lambda job: job.created_at)[:overflow]
    for job in oldest:
      self._jobs.pop(job.job_id, None)
      self._delete_from_disk(job.job_id)

  async def create(self, topic: str) -> QuizJob:
    async with self._lock:
      await self._prune()
      job = QuizJob(job_id=self._new_job_id(), topic=topic)
      self._jobs[job.job_id] = job
      self._persist(job)
      return job

  async def get(self, job_id: str) -> QuizJob | None:
    async with self._lock:
      job = self._get_locked(job_id)
      if job is None:
        return None
      if datetime.now() - job.created_at > self._ttl:
        self._jobs.pop(job_id, None)
        self._delete_from_disk(job_id)
        return None
      return job

  async def mark_running(self, job_id: str, *, quiz_id: str) -> QuizJob | None:
    async with self._lock:
      job = self._get_locked(job_id)
      if job is None:
        return None
      job.status = "running"
      job.quiz_id = quiz_id
      job.updated_at = datetime.now()
      self._persist(job)
      return job

  async def set_preview(self, job_id: str, preview: str) -> QuizJob | None:
    async with self._lock:
      job = self._get_locked(job_id)
      if job is None:
        return None
      job.stream_preview = preview
      job.updated_at = datetime.now()
      now = time.monotonic()
      last = self._preview_last_persist.get(job_id, 0.0)
      if now - last >= PREVIEW_PERSIST_INTERVAL_S:
        self._persist(job)
        self._preview_last_persist[job_id] = now
        self._preview_persist_count += 1
      else:
        self._preview_skip_count += 1
      return job

  def reset_preview_stats(self) -> None:
    self._preview_persist_count = 0
    self._preview_skip_count = 0

  def preview_stats(self) -> tuple[int, int]:
    return self._preview_persist_count, self._preview_skip_count

  async def append_question(self, job_id: str, question: Question) -> QuizJob | None:
    async with self._lock:
      job = self._get_locked(job_id)
      if job is None:
        return None
      if any(existing.id == question.id for existing in job.questions):
        return job
      job.questions.append(question)
      job.updated_at = datetime.now()
      self._persist(job)
      return job

  async def mark_completed(self, job_id: str, result: GenerateQuizResponse) -> QuizJob | None:
    async with self._lock:
      job = self._get_locked(job_id)
      if job is None:
        return None
      job.status = "completed"
      job.quiz_id = result.quiz_id
      job.questions = result.questions
      job.result = result
      job.error = None
      job.updated_at = datetime.now()
      self._persist(job)
      return job

  async def mark_failed(self, job_id: str, error: str) -> QuizJob | None:
    async with self._lock:
      job = self._get_locked(job_id)
      if job is None:
        return None
      job.status = "failed"
      job.error = error
      job.updated_at = datetime.now()
      self._persist(job)
      return job


quiz_job_store = QuizJobStore()
