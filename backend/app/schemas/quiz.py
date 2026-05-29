from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field, field_validator, model_validator


QuestionType = Literal["single", "multiple", "judge"]


class Question(BaseModel):
    id: str
    type: QuestionType
    stem: str
    options: list[str] | None = None
    answer: int | list[int]
    explanation: str

    @field_validator("stem", "explanation")
    @classmethod
    def must_not_be_blank(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("must not be blank")
        return value

    @model_validator(mode="after")
    def validate_by_type(self) -> Question:
        if self.type == "single":
            if not self.options or len(self.options) != 4:
                raise ValueError("single question must have exactly 4 options")
            if not isinstance(self.answer, int) or not 0 <= self.answer < 4:
                raise ValueError("single answer must be an index between 0 and 3")
        elif self.type == "multiple":
            if not self.options or len(self.options) < 4:
                raise ValueError("multiple question must have at least 4 options")
            if not isinstance(self.answer, list) or not self.answer:
                raise ValueError("multiple answer must be a non-empty list")
            max_index = len(self.options) - 1
            if any(not isinstance(item, int) or item < 0 or item > max_index for item in self.answer):
                raise ValueError("multiple answer indices out of range")
        elif self.type == "judge":
            if self.options is None:
                self.options = ["正确", "错误"]
            if len(self.options) != 2:
                raise ValueError("judge question must have exactly 2 options")
            if not isinstance(self.answer, int) or self.answer not in (0, 1):
                raise ValueError("judge answer must be 0 or 1")
        return self


class GenerateQuizRequest(BaseModel):
    topic: str = Field(min_length=1)

    @field_validator("topic")
    @classmethod
    def trim_topic(cls, value: str) -> str:
        trimmed = value.strip()
        if not trimmed:
            raise ValueError("topic must not be blank")
        return trimmed


class GenerateQuizResponse(BaseModel):
    quiz_id: str
    topic: str
    questions: list[Question]

    @model_validator(mode="after")
    def validate_questions(self) -> GenerateQuizResponse:
        if len(self.questions) != 10:
            raise ValueError("questions must contain exactly 10 items")
        ids = [question.id for question in self.questions]
        if len(set(ids)) != len(ids):
            raise ValueError("question ids must be unique")
        return self


class GenerateQuizJobResponse(BaseModel):
    job_id: str
    status: Literal["pending"] = "pending"


class QuizJobStatusResponse(BaseModel):
    job_id: str
    status: Literal["pending", "running", "completed", "failed"]
    quiz_id: str | None = None
    topic: str | None = None
    questions: list[Question] = Field(default_factory=list)
    total_expected: int = 10
    ready: bool = False
    stream_preview: str = ""
    result: GenerateQuizResponse | None = None
    error: str | None = None


class UserAnswer(BaseModel):
    question_id: str
    selected: int | list[int]
    correct: bool


class QuizReportRequest(BaseModel):
    quiz_id: str
    topic: str
    questions: list[Question]
    answers: list[UserAnswer]


class QuizReportResponse(BaseModel):
    score: int
    total: int
    correct_rate: float
    report: str
