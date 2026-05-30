import json

from app.chains.report_generation import _extract_first_json_object, _sanitize_report_text


def _sample_report() -> str:
  return json.dumps(
    {
      "学习复盘报告": {
        "整体表现": "本次练测共10题，仅答对2题。",
        "核心知识点回顾": ["Few-shot 学习"],
        "易错题分析": ["提示词应清晰具体"],
      }
    },
    ensure_ascii=False,
  )


def test_extract_first_json_object_strips_trailing_text() -> None:
  raw = _sample_report() + "\n希望对你有帮助"
  extracted = _extract_first_json_object(raw)
  payload = json.loads(extracted)
  assert payload["学习复盘报告"]["整体表现"]


def test_extract_first_json_object_strips_leading_text() -> None:
  raw = "以下是复盘报告：\n" + _sample_report()
  extracted = _extract_first_json_object(raw)
  payload = json.loads(extracted)
  assert payload["学习复盘报告"]["易错题分析"]


def test_sanitize_report_text_returns_compact_json() -> None:
  raw = _sample_report() + "\n\n以上。"
  cleaned = _sanitize_report_text(raw)
  payload = json.loads(cleaned)
  assert payload["学习复盘报告"]["核心知识点回顾"][0] == "Few-shot 学习"
