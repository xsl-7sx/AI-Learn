import pytest
from fastapi.testclient import TestClient

from app.config import settings
from app.main import app


@pytest.fixture
def client(monkeypatch: pytest.MonkeyPatch):
  monkeypatch.setattr(settings, "mock_llm", True)
  monkeypatch.setattr(settings, "deepseek_api_key", "")
  return TestClient(app)


def test_health(client: TestClient):
  response = client.get("/health")
  assert response.status_code == 200
  assert response.json() == {"status": "ok"}


def test_generate_quiz_returns_ten_questions(client: TestClient):
  response = client.post("/api/v1/quiz/generate", json={"topic": "光合作用"})
  assert response.status_code == 200
  data = response.json()
  assert data["topic"] == "光合作用"
  assert len(data["questions"]) == 10
  types = {question["type"] for question in data["questions"]}
  assert {"single", "multiple", "judge"}.issubset(types)


def test_generate_quiz_rejects_blank_topic(client: TestClient):
  response = client.post("/api/v1/quiz/generate", json={"topic": "   "})
  assert response.status_code == 422


def test_report_returns_markdown(client: TestClient):
  generate = client.post("/api/v1/quiz/generate", json={"topic": "TCP 三次握手"})
  quiz = generate.json()
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
