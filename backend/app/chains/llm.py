from langchain_openai import ChatOpenAI

from app.config import settings


def get_llm(*, json_mode: bool | None = None) -> ChatOpenAI:
  use_json_mode = settings.resolved_json_mode if json_mode is None else json_mode
  model_kwargs: dict = {}
  if use_json_mode:
    model_kwargs["response_format"] = {"type": "json_object"}

  return ChatOpenAI(
    model=settings.resolved_model,
    api_key=settings.resolved_api_key or "mock-key",
    base_url=settings.resolved_base_url,
    temperature=0.7,
    timeout=settings.llm_call_timeout,
    model_kwargs=model_kwargs or None,
  )
