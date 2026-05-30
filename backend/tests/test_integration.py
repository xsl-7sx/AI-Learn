import json

import pytest
from fastapi.testclient import TestClient

from app.config import settings
from app.main import app
from tests.test_api import start_quiz


@pytest.fixture
def client(monkeypatch: pytest.MonkeyPatch):
  monkeypatch.setattr(settings, "mock_llm", True)
  monkeypatch.setattr(settings, "deepseek_api_key", "")
  return TestClient(app)


def test_full_quiz_flow(client: TestClient):
  quiz = start_quiz(client, "光合作用")

  answers = []
  for question in quiz["questions"]:
    answers.append(
      {
        "question_id": question["id"],
        "selected": question["answer"],
        "correct": True,
      }
    )
  answers[0]["selected"] = 0
  answers[0]["correct"] = False

  report = client.post(
    "/api/v1/quiz/report",
    json={
      "quiz_id": quiz["quiz_id"],
      "topic": quiz["topic"],
      "questions": quiz["questions"],
      "answers": answers,
    },
  )
  assert report.status_code == 200
  body = report.json()
  assert body["total"] == 10
  assert body["score"] == 9
  assert body["correct_rate"] == 0.9
  report_payload = json.loads(body["report"])
  assert report_payload["学习复盘报告"]["整体表现"]


def test_async_generate_returns_job_immediately(client: TestClient):
  from tests.test_api import wait_for_quiz_job

  response = client.post("/api/v1/quiz/generate", json={"topic": "异步测试"})
  assert response.status_code == 202
  data = response.json()
  assert data["status"] == "pending"
  assert data["job_id"].startswith("job_")

  status = client.get(f"/api/v1/quiz/jobs/{data['job_id']}")
  assert status.status_code == 200
  assert status.json()["status"] in {"pending", "running", "completed"}

  quiz = wait_for_quiz_job(client, data["job_id"])
  assert len(quiz["questions"]) == 10
