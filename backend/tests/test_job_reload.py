import asyncio

import pytest
from fastapi.testclient import TestClient

from app.jobs import quiz_jobs
from app.jobs.quiz_jobs import QuizJobStore


def test_job_survives_reload_and_api_serves_it(tmp_path, monkeypatch: pytest.MonkeyPatch) -> None:
  monkeypatch.setattr(quiz_jobs, "JOB_DATA_DIR", tmp_path)

  async def seed() -> str:
    store = QuizJobStore()
    job = await store.create("reload-verify")
    await store.mark_running(job.job_id, quiz_id="q_reload_verify")
    return job.job_id

  job_id = asyncio.run(seed())
  assert (tmp_path / f"{job_id}.json").exists()

  reloaded = asyncio.run(QuizJobStore().get(job_id))
  assert reloaded is not None
  assert reloaded.quiz_id == "q_reload_verify"

  from app.config import settings
  from app.main import app

  monkeypatch.setattr(settings, "mock_llm", True)
  monkeypatch.setattr(settings, "deepseek_api_key", "")
  client = TestClient(app)

  response = client.get(f"/api/v1/quiz/jobs/{job_id}")
  assert response.status_code == 200
  assert response.json()["quiz_id"] == "q_reload_verify"
