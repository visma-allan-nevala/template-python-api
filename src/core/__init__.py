"""
Core package for configuration and shared utilities.

This package contains foundational components used throughout the application:
configuration management, constants, custom exceptions, and base utilities.

Modules
-------
config : Configuration management
    Pydantic Settings-based configuration loaded from environment variables.
    Access settings via `from src.core.config import settings`.

constants : Application constants
    Shared constants, enums, and magic values used across the application.

exceptions : Custom exceptions
    Domain-specific exception classes for error handling.
    All custom exceptions inherit from `APIError`.

Usage
-----
Import settings::

    from src.core.config import settings

    if settings.debug:
        print("Debug mode enabled")

Import constants::

    from src.core.constants import DEFAULT_PAGE_SIZE, RiskLevel

Import exceptions::

    from src.core.exceptions import NotFoundError, ValidationError

    raise NotFoundError("User", user_id)

Design Principles
-----------------
1. Configuration is immutable after startup
2. Environment variables are the source of truth
3. Sensible defaults for local development
4. Fail fast on missing required configuration
"""
