from __future__ import annotations

import logging
import os

from dotenv import load_dotenv

logger = logging.getLogger(__name__)

# Load environment variables from .env file
load_dotenv()


def _env_bool(name: str, default: bool = False) -> bool:
    raw = os.getenv(name)
    if raw is None:
        return default
    return raw.strip().lower() in {"1", "true", "yes", "y", "on"}


def _split_csv(value: str) -> list[str]:
    return [part.strip() for part in value.split(",") if part.strip()]


class Settings:
    """Application settings loaded from environment variables.

    Uses os.getenv so missing environment variables never crash on import.
    """

    # Runtime / logging
    DEBUG: bool = _env_bool("DEBUG", False)
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")

    # CORS Configuration (comma-separated)
    CORS_ALLOW_ORIGINS: str = os.getenv("CORS_ALLOW_ORIGINS", "")
    CORS_ALLOW_CREDENTIALS: bool = _env_bool("CORS_ALLOW_CREDENTIALS", False)

    # AI Service Configuration
    GROQ_API_KEY: str = os.getenv("GROQ_API_KEY", "")
    OPENCAGE_API_KEY: str = os.getenv("OPENCAGE_API_KEY", "")
    GOOGLE_API_KEY: str = os.getenv("GOOGLE_API_KEY", "")
    ANTHROPIC_API_KEY: str = os.getenv("ANTHROPIC_API_KEY", "")
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    
    # Database Configuration
    SUPABASE_URL: str = os.getenv("SUPABASE_URL", "")
    SUPABASE_KEY: str = os.getenv("SUPABASE_KEY", "")
    SUPABASE_SERVICE_ROLE_KEY: str = os.getenv("SUPABASE_SERVICE_ROLE_KEY", "")
    
    # Geocoding Configuration
    GEONAMES_USERNAME: str = os.getenv("GEONAMES_USERNAME", "century.boy")

    @property
    def cors_allow_origins_list(self) -> list[str]:
        origins = _split_csv(self.CORS_ALLOW_ORIGINS)
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

# Global settings instance
settings = Settings()

def _legacy_log_startup_info():
    """Legacy startup logging (kept for backward compatibility)."""
    print("🚀 Application Configuration:")
    print(f"  - GROQ_API_KEY loaded: {'Yes' if settings.GROQ_API_KEY else 'No'}")
    print(f"  - CORS_ALLOW_ORIGINS: {settings.CORS_ALLOW_ORIGINS}")
    print(f"  - CORS_ALLOW_CREDENTIALS: {settings.CORS_ALLOW_CREDENTIALS}")
    print(f"  - LOG_LEVEL: {settings.LOG_LEVEL}")
    print(f"  - GEONAMES_USERNAME: {settings.GEONAMES_USERNAME}")
    print(f"  - SUPABASE_URL configured: {'Yes' if settings.SUPABASE_URL else 'No'}")
    print(f"  - GOOGLE_API_KEY configured: {'Yes' if settings.GOOGLE_API_KEY else 'No'}")
    print()


def log_startup_info() -> None:
    """Log startup information (without printing secret values)."""
    logger.info("Application configuration:")
    logger.info("  GROQ_API_KEY configured: %s", "Yes" if settings.GROQ_API_KEY else "No")
    logger.info("  OPENCAGE_API_KEY configured: %s", "Yes" if settings.OPENCAGE_API_KEY else "No")
    logger.info("  SUPABASE_URL configured: %s", "Yes" if settings.SUPABASE_URL else "No")
    logger.info("  SUPABASE_KEY configured: %s", "Yes" if settings.supabase_key_effective else "No")
    logger.info("  CORS_ALLOW_ORIGINS: %s", settings.CORS_ALLOW_ORIGINS or "(empty)")
    logger.info("  CORS_ALLOW_CREDENTIALS: %s", settings.CORS_ALLOW_CREDENTIALS)
    logger.info("  LOG_LEVEL: %s", settings.LOG_LEVEL)
