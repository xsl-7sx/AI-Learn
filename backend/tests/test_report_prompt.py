from langchain_core.prompts import ChatPromptTemplate

from app.prompts.report_generation import REPORT_GENERATION_SYSTEM, REPORT_GENERATION_USER


def test_report_prompt_template_escapes_json_braces() -> None:
  prompt = ChatPromptTemplate.from_messages(
    [
      ("system", REPORT_GENERATION_SYSTEM),
      ("human", REPORT_GENERATION_USER),
    ]
  )
  rendered = prompt.format(topic="RAG", answers_summary="- [错误] 示例题干")
  assert "学习复盘报告" in rendered
  assert "{topic}" not in rendered
  assert "RAG" in rendered
