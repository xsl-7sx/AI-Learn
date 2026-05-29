import time

import pytest
from fastapi.testclient import TestClient

from app.config import settings
from app.main import app


@pytest.fixture
def client(monkeypatch: pytest.MonkeyPatch):
  monkeypatch.setattr(settings, "mock_llm", True)
  monkeypatch.setattr(settings, "deepseek_api_key", "")
  return TestClient(app)


def wait_for_quiz_job(client: TestClient, job_id: str, *, max_attempts: int = 50) -> dict:
  for _ in range(max_attempts):
    response = client.get(f"/api/v1/quiz/jobs/{job_id}")
    assert response.status_code == 200
    data = response.json()
    if data["status"] == "completed":
      assert data["result"] is not None
      return data["result"]
    if data["status"] == "failed":
      pytest.fail(data.get("error") or "quiz job failed")
    time.sleep(0.05)
  pytest.fail("quiz job timed out in test")


def start_quiz(client: TestClient, topic: str) -> dict:
  response = client.post("/api/v1/quiz/generate", json={"topic": topic})
  assert response.status_code == 202
  job = response.json()
  return wait_for_quiz_job(client, job["job_id"])


def test_health(client: TestClient):
  response = client.get("/health")
  assert response.status_code == 200
  assert response.json() == {"status": "ok"}


def test_generate_quiz_returns_ten_questions(client: TestClient):
  data = start_quiz(client, "光合作用")
  assert data["topic"] == "光合作用"
  assert len(data["questions"]) == 10
  types = {question["type"] for question in data["questions"]}
  assert {"single", "multiple", "judge"}.issubset(types)


def test_generate_quiz_rejects_blank_topic(client: TestClient):
  response = client.post("/api/v1/quiz/generate", json={"topic": "   "})
  assert response.status_code == 422


def test_generate_quiz_job_not_found(client: TestClient):
  response = client.get("/api/v1/quiz/jobs/job_missing")
  assert response.status_code == 404


def test_report_returns_markdown(client: TestClient):
  quiz = start_quiz(client, "TCP 三次握手")
  answers = [
    {
      "question_id": question["id"],
      "selected": question["answer"],
      "correct": True,
    }
    for question in quiz["questions"]
  ]
  response = client.post(
    "/api/v1/quiz/report",
    json={
      "quiz_id": quiz["quiz_id"],
      "topic": quiz["topic"],
      "questions": quiz["questions"],
      "answers": answers,
    },
  )
  assert response.status_code == 200
  data = response.json()
  assert data["total"] == 10
  assert data["score"] == 10
  assert data["correct_rate"] == 1.0
  assert "##" in data["report"]
