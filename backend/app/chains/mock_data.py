from __future__ import annotations

from datetime import datetime
from uuid import uuid4

from app.schemas.quiz import GenerateQuizResponse, Question


def _make_questions(topic: str) -> list[Question]:
  return [
    Question(
      id="q1",
      type="single",
      stem=f"关于「{topic}」，下列哪项描述最准确？",
      options=["选项 A", "选项 B", "选项 C", "选项 D"],
      answer=1,
      explanation="这是单选题解析示例：先抓住题干关键词，再排除明显不符的选项。"
    ),
    Question(
      id="q2",
      type="multiple",
      stem=f"以下哪些与「{topic}」直接相关？",
      options=["概念一", "概念二", "概念三", "概念四"],
      answer=[0, 2],
      explanation="多选题要看全：漏选或多选都会错，把每个选项和题干逐一对照。"
    ),
    Question(
      id="q3",
      type="judge",
      stem=f"「{topic}」只需要记住定义，不需要理解应用场景。",
      options=["正确", "错误"],
      answer=1,
      explanation="只背定义不够，得能说出一两个真实应用场景，才算真懂。"
    ),
    *[
      Question(
        id=f"q{i}",
        type="single",
        stem=f"第 {i} 题：{topic} 相关练习",
        options=["选项 A", "选项 B", "选项 C", "选项 D"],
        answer=(i - 1) % 4,
        explanation=f"第 {i} 题解析。",
      )
      for i in range(4, 11)
    ],
  ]


def build_mock_quiz(topic: str) -> GenerateQuizResponse:
  return GenerateQuizResponse(
    quiz_id=f"q_{datetime.now().strftime('%Y%m%d')}_{uuid4().hex[:8]}",
    topic=topic,
    questions=_make_questions(topic),
  )


MOCK_REPORT = """## 整体表现

本次练测完成度不错，已覆盖核心概念。

## 核心知识点回顾

- 先回顾主题定义与关键术语
- 再串联典型应用场景

## 易错题分析

- 多选题注意「全对才得分」
- 判断题要区分绝对化表述

## 复习建议

1. 用 3 句话复述今天主题
2. 明天再做一组同类题巩固
"""
