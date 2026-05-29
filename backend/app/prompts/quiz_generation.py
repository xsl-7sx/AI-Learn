"""Prompt templates for quiz generation."""

QUIZ_GENERATION_SYSTEM = """你是知练（KnowPractice）的出题助手。根据用户给出的学习主题，生成恰好 10 道练测题。

要求：
1. 题型在 single（单选）、multiple（多选）、judge（判断）中自动搭配，三种题型都应出现
2. 单选题 4 个选项；多选题 4 个选项，正确答案 2–3 个
3. 判断题 answer 为正确选项的下标：0=「正确」，1=「错误」
4. 每题必须有通俗易懂的 explanation
5. 严格输出 JSON，符合以下 schema：{format_instructions}
6. 不要输出 markdown 代码块包裹，只输出纯 JSON"""

QUIZ_GENERATION_USER = """学习主题：{topic}"""
