"""MVP 验收闸门自动化测试（G1 / G3 / G4 后端部分）。

对照文档：docs/MVP开发实施指南.md §一、§三
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from app.chains.mock_data import build_mock_quiz
from app.config import settings
from app.main import app
from tests.test_api import start_quiz, wait_for_quiz_job, wait_until_job_ready


@pytest.fixture
def client(monkeypatch: pytest.MonkeyPatch):
  monkeypatch.setattr(settings, "mock_llm", True)
  monkeypatch.setattr(settings, "deepseek_api_key", "")
  return TestClient(app)


# --- G1：后端 generate / report 接口 ---


def test_g1_health_endpoint(client: TestClient):
  """G1：/health 可用，暴露 llm_mode。"""
  response = client.get("/health")
  assert response.status_code == 200
  body = response.json()
  assert body["status"] == "ok"
  assert body["llm_mode"] in ("mock", "live")


def test_g1_generate_returns_job_202(client: TestClient):
  """G1：POST /generate 返回 202 + job_id。"""
  response = client.post("/api/v1/quiz/generate", json={"topic": "MVP验收"})
  assert response.status_code == 202
  data = response.json()
  assert data["job_id"].startswith("job_")
  assert data["status"] == "pending"


def test_g1_quiz_has_ten_questions_and_three_types(client: TestClient):
  """G1：完成态含 10 题，且 single/multiple/judge 均出现。"""
  quiz = start_quiz(client, "MVP验收")
  assert len(quiz["questions"]) == 10
  types = {q["type"] for q in quiz["questions"]}
  assert types == {"single", "multiple", "judge"}


def test_g1_report_returns_structured_json(client: TestClient):
  """G1/G4：POST /report 返回可解析的结构化 JSON 复盘。"""
  quiz = start_quiz(client, "MVP验收")
  answers = [
    {"question_id": q["id"], "selected": q["answer"], "correct": True}
    for q in quiz["questions"]
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
  body = response.json()
  assert body["total"] == 10
  report = json.loads(body["report"])
  mini = report["学习复盘报告"]
  assert mini["整体表现"]
  assert isinstance(mini["核心知识点回顾"], list)
  assert isinstance(mini["易错题分析"], list)


# --- G3：流式出题 + 首题就绪 ---


def test_g3_streaming_first_question_ready_before_complete(client: TestClient):
  """G3：首题就绪（ready + questions>=1）可在 completed 之前发生。"""
  response = client.post("/api/v1/quiz/generate", json={"topic": "流式MVP"})
  job_id = response.json()["job_id"]

  ready = wait_until_job_ready(client, job_id)
  assert ready["ready"] is True
  assert len(ready["questions"]) >= 1
  assert ready["total_expected"] == 10

  completed = wait_for_quiz_job(client, job_id)
  assert len(completed["questions"]) == 10


def test_g3_mock_quiz_fixture_matches_contract():
  """G3：Mock 出题链固定 10 题且字段齐全。"""
  quiz = build_mock_quiz("测试主题")
  assert quiz.topic == "测试主题"
  assert len(quiz.questions) == 10
  for question in quiz.questions:
    assert question.stem
    assert question.explanation


# --- G4：完整闭环 ---


def test_g4_full_closed_loop_generate_answer_report(client: TestClient):
  """G4：generate → 10 题 → report 计分与 JSON 复盘一次通过。"""
  quiz = start_quiz(client, "闭环验收")
  answers = []
  for index, question in enumerate(quiz["questions"]):
    answers.append(
      {
        "question_id": question["id"],
        "selected": question["answer"],
        "correct": index != 0,
      }
    )

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
  body = response.json()
  assert body["score"] == 9
  assert body["correct_rate"] == 0.9
  report = json.loads(body["report"])
  assert report["学习复盘报告"]["整体表现"]


def test_g4_openapi_documents_mvp_endpoints(client: TestClient):
  """G4：OpenAPI 暴露 MVP 三个核心端点。"""
  response = client.get("/openapi.json")
  assert response.status_code == 200
  paths = response.json()["paths"]
  assert "/api/v1/quiz/generate" in paths
  assert "/api/v1/quiz/jobs/{job_id}" in paths
  assert "/api/v1/quiz/report" in paths


def test_repo_has_mvp_frontend_pages():
  """G0 静态：四页面源码与 pages.json 注册一致（跨端校验）。"""
  repo_root = Path(__file__).resolve().parents[2]
  pages_json = repo_root / "uniapp" / "src" / "pages.json"
  assert pages_json.exists()
  data = json.loads(pages_json.read_text(encoding="utf-8"))
  routes = [page["path"] for page in data["pages"]]
  assert routes == [
    "pages/index/index",
    "pages/loading/loading",
    "pages/quiz/quiz",
    "pages/result/result",
  ]
  for route in routes:
    vue_path = repo_root / "uniapp" / "src" / f"{route}.vue"
    assert vue_path.exists(), f"missing page file: {vue_path}"
