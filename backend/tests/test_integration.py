import pytest
from fastapi.testclient import TestClient

from app.config import settings
from app.main import app


@pytest.fixture
def client(monkeypatch: pytest.MonkeyPatch):
  monkeypatch.setattr(settings, "mock_llm", True)
  monkeypatch.setattr(settings, "deepseek_api_key", "")
  return TestClient(app)


def test_full_quiz_flow(client: TestClient):
  generate = client.post("/api/v1/quiz/generate", json={"topic": "光合作用"})
  assert generate.status_code == 200
  quiz = generate.json()

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
  assert "整体表现" in body["report"] or "##" in body["report"]
