import json

from app.chains.quiz_stream_generation import (
  _missing_question_ids,
  _salvage_questions_from_text,
  _sort_questions_by_id,
)
from app.schemas.quiz import Question


def _q(qid: str) -> Question:
  return Question(
    id=qid,
    type="single",
    stem=f"题干{qid}",
    options=["A", "B", "C", "D"],
    answer=0,
    explanation="解析",
  )


def test_missing_question_ids():
  collected = [_q("q1"), _q("q2"), _q("q4")]
  assert _missing_question_ids(collected) == ["q3", "q5", "q6", "q7", "q8", "q9", "q10"]


def test_salvage_questions_from_text():
  payload = {
    "id": "q3",
    "type": "judge",
    "stem": "判断题",
    "answer": 1,
    "explanation": "解析",
  }
  text = f"prefix garbage {json.dumps(payload, ensure_ascii=False)} suffix"
  seen: set[str] = set()
  found = _salvage_questions_from_text(text, seen)
  assert len(found) == 1
  assert found[0].id == "q3"


def test_sort_questions_by_id():
  ordered = _sort_questions_by_id([_q("q10"), _q("q2"), _q("q1")])
  assert [item.id for item in ordered] == ["q1", "q2", "q10"]
