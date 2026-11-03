"""
Centralized settings — all values loaded from environment variables.
"""
from functools import lru_cache
from typing import Literal
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # ── App ──────────────────────────────────────────────────────────
    app_name: str        = "AI Research Report Agent"
    app_version: str     = "2.0.0"
    app_env: Literal["development", "production"] = "development"
    api_prefix: str      = "/api/v1"

    # ── Server ───────────────────────────────────────────────────────
    host: str  = "0.0.0.0"
    port: int  = 8000

    # ── LLM providers ────────────────────────────────────────────────
    groq_api_key: str    = ""
    openai_api_key: str  = ""
    groq_model: str      = "llama-3.3-70b-versatile"
    openai_model: str    = "gpt-4o-mini"

    # ── Search ───────────────────────────────────────────────────────
    tavily_api_key: str  = ""
    search_max_results: int = 5
    search_depth: Literal["basic", "advanced"] = "advanced"

    # ── Agent ────────────────────────────────────────────────────────
    max_query_length: int = 500

    # ── Logging ──────────────────────────────────────────────────────
    log_level: str = "INFO"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    @property
    def is_production(self) -> bool:
        return self.app_env == "production"


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
