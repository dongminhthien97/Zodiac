from __future__ import annotations

import logging
from functools import lru_cache

from dotenv import load_dotenv
from pydantic_settings import BaseSettings, SettingsConfigDict

logger = logging.getLogger(__name__)

# Local dev: load `.env` if present. Railway: values come from the Variables tab.
load_dotenv(override=False)


def _split_csv(value: str) -> list[str]:
    return [part.strip() for part in value.split(",") if part.strip()]


class Settings(BaseSettings):
    """Application settings (Railway + local `.env`)."""

    model_config = SettingsConfigDict(extra="ignore")

    DEBUG: bool = False
    LOG_LEVEL: str = "INFO"

    CORS_ALLOW_ORIGINS: str = ""
    CORS_ALLOW_CREDENTIALS: bool = False

    GROQ_API_KEY: str = ""
    OPENCAGE_API_KEY: str = ""
    GOOGLE_API_KEY: str = ""
    ANTHROPIC_API_KEY: str = ""
    OPENAI_API_KEY: str = ""

    SUPABASE_URL: str = ""
    SUPABASE_KEY: str = ""
    SUPABASE_SERVICE_ROLE_KEY: str = ""

    GEONAMES_USERNAME: str = "century.boy"

    # If true, fail startup when required env vars are missing.
    STRICT_ENV: bool = False

    @property
    def cors_allow_origins_list(self) -> list[str]:
        origins = _split_csv(self.CORS_ALLOW_ORIGINS or "")
        if not origins and self.DEBUG:
            origins = [
                "http://localhost:5173",
                "http://127.0.0.1:5173",
                "http://localhost:3000",
                "http://127.0.0.1:3000",
            ]

        if self.CORS_ALLOW_CREDENTIALS and "*" in origins:
            logger.warning(
                "CORS_ALLOW_CREDENTIALS=true but CORS_ALLOW_ORIGINS contains '*'; removing wildcard origin."
            )
            origins = [o for o in origins if o != "*"]

        return origins

    @property
    def supabase_key_effective(self) -> str:
        return self.SUPABASE_SERVICE_ROLE_KEY or self.SUPABASE_KEY

    def missing_required(self) -> list[str]:
        """Return missing env vars for core features."""
        missing: list[str] = []
        if not self.OPENCAGE_API_KEY:
            missing.append("OPENCAGE_API_KEY")
        if not self.GROQ_API_KEY:
            missing.append("GROQ_API_KEY")
        return missing


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings()


settings = get_settings()


def log_startup_info() -> None:
    """Log startup information (without printing secret values)."""
    s = get_settings()
    logger.info("Startup configuration:")
    logger.info("  DEBUG: %s", s.DEBUG)
    logger.info("  LOG_LEVEL: %s", s.LOG_LEVEL)
    logger.info("  CORS_ALLOW_ORIGINS set: %s", "Yes" if s.CORS_ALLOW_ORIGINS else "No")
    logger.info("  CORS_ALLOW_CREDENTIALS: %s", s.CORS_ALLOW_CREDENTIALS)
    logger.info("  GROQ_API_KEY configured: %s", "Yes" if s.GROQ_API_KEY else "No")
    logger.info("  OPENCAGE_API_KEY configured: %s", "Yes" if s.OPENCAGE_API_KEY else "No")
    logger.info("  SUPABASE_URL configured: %s", "Yes" if s.SUPABASE_URL else "No")
    logger.info("  SUPABASE_KEY configured: %s", "Yes" if s.supabase_key_effective else "No")
    logger.info("  GEONAMES_USERNAME: %s", s.GEONAMES_USERNAME)
