from app.chains.llm import get_llm


def test_get_llm_without_json_mode():
  llm = get_llm(json_mode=False)
  assert isinstance(llm, object)


def test_get_llm_with_json_mode():
  llm = get_llm(json_mode=True)
  assert llm.model_kwargs.get("response_format") == {"type": "json_object"}
