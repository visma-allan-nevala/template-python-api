"""
Application Configuration.

Manages application settings loaded from environment variables using Pydantic Settings.
All configuration is validated at startup and accessible via the `settings` singleton.

Usage
-----
Import and use the settings singleton::

    from src.core.config import settings

    print(settings.app_name)
    print(settings.database.host)

Environment Variables
---------------------
Settings are loaded from environment variables. See `.env.example` for all options.

Common patterns:
- Simple values: `APP_NAME=my-api`
- Nested settings: `DATABASE_HOST=localhost` (underscore separates levels)
- Lists: `CORS_ORIGINS=http://localhost:3000,http://localhost:8080`
- Secrets: Use environment variables or secret managers

Configuration Hierarchy
-----------------------
1. Environment variables (highest priority)
2. `.env` file (if present)
3. Default values in Settings class (lowest priority)

Adding New Settings
-------------------
1. Add field to appropriate Settings class
2. Set a sensible default if possible
3. Document the environment variable in `.env.example`
4. Use `Field()` for validation constraints

Example::

    class Settings(BaseSettings):
        new_setting: str = Field(
            default="default_value",
            description="Description of the setting",
        )
"""

from functools import lru_cache
from typing import Any

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class DatabaseSettings(BaseSettings):
    """Database connection settings."""

    model_config = SettingsConfigDict(
        env_prefix="DATABASE_",
        extra="ignore",
    )

    host: str = Field(default="localhost", description="Database host")
    port: int = Field(default=5432, description="Database port")
    user: str = Field(default="app_user", description="Database user")
    password: str = Field(default="app_password", description="Database password")
    name: str = Field(default="app_db", description="Database name")
    ssl: bool = Field(default=False, description="Enable SSL connection")

    @property
    def url(self) -> str:
        """Construct database URL."""
        ssl_suffix = "?ssl=require" if self.ssl else ""
        return f"postgresql+asyncpg://{self.user}:{self.password}@{self.host}:{self.port}/{self.name}{ssl_suffix}"


class RedisSettings(BaseSettings):
    """Redis connection settings."""

    model_config = SettingsConfigDict(
        env_prefix="REDIS_",
        extra="ignore",
    )

    host: str = Field(default="localhost", description="Redis host")
    port: int = Field(default=6379, description="Redis port")
    db: int = Field(default=0, description="Redis database number")
    password: str | None = Field(default=None, description="Redis password")

    @property
    def url(self) -> str:
        """Construct Redis URL."""
        auth = f":{self.password}@" if self.password else ""
        return f"redis://{auth}{self.host}:{self.port}/{self.db}"


class Settings(BaseSettings):
    """
    Application settings.

    Loaded from environment variables with optional `.env` file support.
    Access via `from src.core.config import settings`.
    """

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
        case_sensitive=False,
    )

    # Application
    app_name: str = Field(default="my-api", description="Application name")
    app_env: str = Field(default="local", description="Environment (local/dev/staging/prod)")
    debug: bool = Field(default=False, description="Enable debug mode")

    # Server
    api_host: str = Field(default="0.0.0.0", description="API host")
    api_port: int = Field(default=8000, description="API port")

    # Security
    api_keys: list[str] = Field(default_factory=list, description="Valid API keys")
    secret_key: str = Field(
        default="change-me-in-production",
        description="Secret key for signing",
    )

    # CORS
    cors_origins: list[str] = Field(
        default_factory=lambda: ["http://localhost:3000"],
        description="Allowed CORS origins",
    )

    # Logging
    log_level: str = Field(default="INFO", description="Log level")
    log_format: str = Field(default="text", description="Log format (text/json)")

    # Nested settings
    database: DatabaseSettings = Field(default_factory=DatabaseSettings)
    redis: RedisSettings = Field(default_factory=RedisSettings)

    @field_validator("api_keys", mode="before")
    @classmethod
    def parse_api_keys(cls, v: Any) -> list[str]:
        """Parse comma-separated API keys."""
        if isinstance(v, str):
            return [k.strip() for k in v.split(",") if k.strip()]
        return v or []

    @field_validator("cors_origins", mode="before")
    @classmethod
    def parse_cors_origins(cls, v: Any) -> list[str]:
        """Parse comma-separated CORS origins."""
        if isinstance(v, str):
            return [o.strip() for o in v.split(",") if o.strip()]
        return v or []

    @property
    def is_production(self) -> bool:
        """Check if running in production environment."""
        return self.app_env in ("production", "prod")

    @property
    def is_development(self) -> bool:
        """Check if running in development environment."""
        return self.app_env in ("development", "dev", "local")


@lru_cache
def get_settings() -> Settings:
    """
    Get cached settings instance.

    Returns
    -------
    Settings
        Application settings singleton
    """
    return Settings()


# Settings singleton for easy import
settings = get_settings()
