from typing import Literal

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
  model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

  # 供应商：deepseek（推荐）| zhipu | auto（有 LLM_API_KEY 用智谱，否则 DeepSeek）
  llm_provider: Literal["deepseek", "zhipu", "auto"] = Field(
    default="auto",
    validation_alias="LLM_PROVIDER",
  )

  # 通用 LLM（OpenAI 兼容：智谱 / DeepSeek 等）
  llm_api_key: str = Field(default="", validation_alias="LLM_API_KEY")
  llm_model: str = Field(default="glm-4.5-air", validation_alias="LLM_MODEL")
  llm_base_url: str = Field(
    default="https://open.bigmodel.cn/api/paas/v4",
    validation_alias="LLM_BASE_URL",
  )

  # DeepSeek（方案 B 推荐）
  deepseek_api_key: str = ""
  deepseek_model: str = "deepseek-chat"
  deepseek_base_url: str = "https://api.deepseek.com/v1"

  llm_json_mode: bool = Field(default=True, validation_alias="LLM_JSON_MODE")
  llm_call_timeout: int = 120
  request_total_timeout: int = 180
  mock_llm: bool = False

  @property
  def resolved_api_key(self) -> str:
    if self.llm_provider == "deepseek":
      return self.deepseek_api_key
    if self.llm_provider == "zhipu":
      return self.llm_api_key
    return self.llm_api_key or self.deepseek_api_key

  @property
  def resolved_model(self) -> str:
    if self.llm_provider == "deepseek":
      return self.deepseek_model
    if self.llm_provider == "zhipu":
      return self.llm_model
    if self.llm_api_key:
      return self.llm_model
    if self.deepseek_api_key:
      return self.deepseek_model
    return self.llm_model

  @property
  def resolved_base_url(self) -> str:
    if self.llm_provider == "deepseek":
      return self.deepseek_base_url
    if self.llm_provider == "zhipu":
      return self.llm_base_url
    if self.llm_api_key:
      return self.llm_base_url
    if self.deepseek_api_key:
      return self.deepseek_base_url
    return self.llm_base_url

  @property
  def resolved_json_mode(self) -> bool:
    if self.mock_llm or not self.resolved_api_key:
      return False
    return self.llm_json_mode


settings = Settings()
