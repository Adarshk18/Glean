"""
config.py
---------
Centralized application configuration.

WHY THIS FILE EXISTS:
Every secret/config value (database URL, API keys, JWT secret, etc.) is
defined ONCE here as a typed field on the `Settings` class. Pydantic reads
the values from the `.env` file, validates their types, and raises a clear
error immediately on startup if something is missing or malformed.

Every other file in the app imports the single `settings` object from here
instead of reading os.environ directly. This means:
  1. One source of truth for all configuration.
  2. Type safety - e.g. ACCESS_TOKEN_EXPIRE_MINUTES is guaranteed to be an
     int, not a string, by the time any code uses it.
  3. Fail-fast behavior - a missing required variable crashes the app at
     startup with a clear message, not deep inside a request handler later.
"""

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # -------------------------------------------------
    # Environment
    # -------------------------------------------------
    ENVIRONMENT: str = "development"

    # -------------------------------------------------
    # Database (PostgreSQL)
    # -------------------------------------------------
    DATABASE_URL: str

    # -------------------------------------------------
    # Auth / JWT
    # -------------------------------------------------
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

    # -------------------------------------------------
    # OpenAI (LLM + Embeddings)
    # -------------------------------------------------
    OPENAI_API_KEY: str
    OPENAI_CHAT_MODEL: str = "gpt-4o-mini"
    OPENAI_EMBEDDING_MODEL: str = "text-embedding-3-small"

    # -------------------------------------------------
    # Vector database (Qdrant)
    # -------------------------------------------------
    QDRANT_URL: str = "http://localhost:6333"
    QDRANT_API_KEY: str = ""
    QDRANT_COLLECTION_NAME: str = "document_chunks"

    # -------------------------------------------------
    # Tells pydantic-settings WHERE to load values from
    # -------------------------------------------------
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
    )


# A single, shared instance of Settings.
# Every other file does: `from app.config import settings`
# and then uses e.g. `settings.DATABASE_URL`
settings = Settings()