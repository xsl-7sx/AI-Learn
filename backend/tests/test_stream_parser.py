import json

from app.chains.quiz_stream_generation import QuestionStreamParser
from app.schemas.quiz import Question


def test_question_stream_parser_reads_jsonl_lines():
  parser = QuestionStreamParser()
  chunk1 = (
    '{"id":"q1","type":"single","stem":"题干1","options":["A","B","C","D"],'
  )
  chunk2 = (
    '"answer":1,"explanation":"解析1"}\n'
    '{"id":"q2","type":"judge","stem":"题干2","answer":0,"explanation":"解析2"}\n'
  )

  first = parser.feed(chunk1)
  assert first == []

  second = parser.feed(chunk2)
  assert len(second) == 2
  assert second[0].id == "q1"
  assert second[1].id == "q2"


def test_question_stream_parser_deduplicates_ids():
  parser = QuestionStreamParser()
  line = json.dumps(
    {
      "id": "q1",
      "type": "single",
      "stem": "题干",
      "options": ["A", "B", "C", "D"],
      "answer": 0,
      "explanation": "解析",
    },
    ensure_ascii=False,
  )
  first = parser.feed(f"{line}\n")
  second = parser.feed(f"{line}\n")
  assert len(first) == 1
  assert second == []
  assert isinstance(first[0], Question)
