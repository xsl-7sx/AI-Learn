from __future__ import annotations

import json
import re
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


def build_mock_report(
  *,
  topic: str,
  score: int,
  total: int,
  wrong_stems: list[str],
) -> str:
  rate = round(score / total * 100) if total else 0
  if rate >= 80:
    overview = f"「{topic}」练测表现优秀，答对 {score}/{total} 题（{rate}%），核心概念掌握扎实。"
  elif rate >= 50:
    overview = f"「{topic}」练测完成，答对 {score}/{total} 题（{rate}%），基础已有，错题值得再巩固。"
  else:
    overview = f"「{topic}」练测完成，答对 {score}/{total} 题（{rate}%），别灰心，抓住错题就是进步。"

  wrong_analysis = wrong_stems[:3] if wrong_stems else ["本次错题较少，继续保持审题习惯"]

  payload = {
    "学习复盘报告": {
      "整体表现": overview,
      "核心知识点回顾": [
        f"回顾「{topic}」的定义与关键术语",
        "把错题解析用自己的话复述一遍",
      ],
      "易错题分析": wrong_analysis,
      "复习建议": [
        "明天再做一组同类题巩固",
        "多选题注意「全对才得分」",
      ],
    },
  }
  return json.dumps(payload, ensure_ascii=False)


# 兼容旧引用；新逻辑请用 build_mock_report
MOCK_REPORT = build_mock_report(topic="示例主题", score=7, total=10, wrong_stems=["示例错题"])
