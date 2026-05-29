import pytest
from pydantic import ValidationError

from app.schemas.quiz import (
    GenerateQuizRequest,
    GenerateQuizResponse,
    Question,
    QuizReportRequest,
    UserAnswer,
)


def _single_question(**overrides) -> dict:
    base = {
        "id": "q1",
        "type": "single",
        "stem": "光合作用的主要场所是？",
        "options": ["线粒体", "叶绿体", "细胞核", "液泡"],
        "answer": 1,
        "explanation": "叶绿体含有叶绿素，是光合作用的主要场所。",
    }
    base.update(overrides)
    return base


def _ten_questions(**overrides) -> list[dict]:
    questions = []
    for i in range(10):
        q = _single_question(id=f"q{i + 1}")
        if i == 1:
            q.update(
                {
                    "type": "multiple",
                    "stem": "以下属于传输层协议的有？",
                    "options": ["TCP", "UDP", "IP", "HTTP"],
                    "answer": [0, 1],
                }
            )
        if i == 2:
            q.update(
                {
                    "type": "judge",
                    "stem": "TCP 使用四次握手建立连接。",
                    "options": ["正确", "错误"],
                    "answer": 1,
                }
            )
        q.update(overrides)
        questions.append(q)
    return questions


def test_valid_single_question():
    question = Question.model_validate(_single_question())
    assert question.type == "single"
    assert question.answer == 1


def test_single_answer_out_of_range_raises():
    with pytest.raises(ValidationError):
        Question.model_validate(_single_question(answer=4))


def test_multiple_answer_must_be_list():
    with pytest.raises(ValidationError):
        Question.model_validate(
            _single_question(
                type="multiple",
                options=["A", "B", "C", "D"],
                answer=0,
            )
        )


def test_judge_answer_out_of_range_raises():
    with pytest.raises(ValidationError):
        Question.model_validate(
            _single_question(
                type="judge",
                options=["正确", "错误"],
                answer=2,
            )
        )


def test_generate_quiz_requires_ten_questions():
    with pytest.raises(ValidationError):
        GenerateQuizResponse.model_validate(
            {
                "quiz_id": "q_test",
                "topic": "光合作用",
                "questions": _ten_questions()[:9],
            }
        )


def test_duplicate_question_ids_raise():
    questions = _ten_questions()
    questions[1]["id"] = "q1"
    with pytest.raises(ValidationError):
        GenerateQuizResponse.model_validate(
            {
                "quiz_id": "q_test",
                "topic": "光合作用",
                "questions": questions,
            }
        )


def test_generate_request_topic_trimmed():
    req = GenerateQuizRequest.model_validate({"topic": "  光合作用  "})
    assert req.topic == "光合作用"


def test_report_request_accepts_answers():
    payload = QuizReportRequest.model_validate(
        {
            "quiz_id": "q_test",
            "topic": "光合作用",
            "questions": _ten_questions(),
            "answers": [
                UserAnswer(
                    question_id="q1",
                    selected=1,
                    correct=True,
                ).model_dump()
            ],
        }
    )
    assert payload.answers[0].correct is True
