import asyncio

import pytest

from app.jobs import quiz_jobs


def test_quiz_job_persists_to_disk(tmp_path, monkeypatch: pytest.MonkeyPatch) -> None:
  monkeypatch.setattr(quiz_jobs, "JOB_DATA_DIR", tmp_path)

  async def run() -> None:
    store1 = quiz_jobs.QuizJobStore()
    job = await store1.create("持久化测试")
    await store1.mark_running(job.job_id, quiz_id="q_persist_test")

    store2 = quiz_jobs.QuizJobStore()
    loaded = await store2.get(job.job_id)
    assert loaded is not None
    assert loaded.topic == "持久化测试"
    assert loaded.quiz_id == "q_persist_test"
    assert loaded.status == "running"

  asyncio.run(run())
