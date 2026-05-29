from langchain_openai import ChatOpenAI

from app.config import settings


def get_llm() -> ChatOpenAI:
  return ChatOpenAI(
    model=settings.resolved_model,
    api_key=settings.resolved_api_key or "mock-key",
    base_url=settings.resolved_base_url,
    temperature=0.7,
    timeout=settings.llm_call_timeout,
  )
