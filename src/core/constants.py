"""
Application Constants.

Centralized location for all constants, enums, and magic values used throughout
the application. This makes it easy to find and modify values.

Usage
-----
Import constants::

    from src.core.constants import DEFAULT_PAGE_SIZE, MAX_PAGE_SIZE
    from src.core.constants import Status, ErrorCode

Guidelines
----------
1. Use UPPER_CASE for module-level constants
2. Use Enum classes for related choices
3. Add docstrings explaining the purpose
4. Group related constants together
"""

from enum import Enum

# =============================================================================
# Pagination
# =============================================================================

DEFAULT_PAGE_SIZE = 20
"""Default number of items per page."""

MAX_PAGE_SIZE = 100
"""Maximum allowed items per page."""

MIN_PAGE_SIZE = 1
"""Minimum allowed items per page."""


# =============================================================================
# Rate Limiting
# =============================================================================

DEFAULT_RATE_LIMIT = 100
"""Default requests per minute per client."""

RATE_LIMIT_WINDOW_SECONDS = 60
"""Rate limit time window in seconds."""


# =============================================================================
# Timeouts
# =============================================================================

DEFAULT_TIMEOUT_SECONDS = 30
"""Default timeout for external API calls."""

DATABASE_TIMEOUT_SECONDS = 10
"""Timeout for database operations."""

CACHE_TTL_SECONDS = 300
"""Default cache time-to-live (5 minutes)."""


# =============================================================================
# Enums
# =============================================================================


class Status(str, Enum):
    """Generic status values."""

    ACTIVE = "active"
    INACTIVE = "inactive"
    PENDING = "pending"
    DELETED = "deleted"


class Environment(str, Enum):
    """Application environments."""

    LOCAL = "local"
    DEVELOPMENT = "development"
    STAGING = "staging"
    PRODUCTION = "production"


class ErrorCode(str, Enum):
    """Standard error codes for API responses."""

    # Client errors (4xx)
    BAD_REQUEST = "BAD_REQUEST"
    UNAUTHORIZED = "UNAUTHORIZED"
    FORBIDDEN = "FORBIDDEN"
    NOT_FOUND = "NOT_FOUND"
    CONFLICT = "CONFLICT"
    VALIDATION_ERROR = "VALIDATION_ERROR"
    RATE_LIMITED = "RATE_LIMITED"

    # Server errors (5xx)
    INTERNAL_ERROR = "INTERNAL_ERROR"
    SERVICE_UNAVAILABLE = "SERVICE_UNAVAILABLE"
    GATEWAY_TIMEOUT = "GATEWAY_TIMEOUT"


class SortOrder(str, Enum):
    """Sort order options."""

    ASC = "asc"
    DESC = "desc"


# =============================================================================
# String Constants
# =============================================================================

API_VERSION = "v1"
"""Current API version."""

HEALTH_CHECK_PATH = "/api/v1/health"
"""Health check endpoint path."""

DATE_FORMAT = "%Y-%m-%d"
"""Standard date format."""

DATETIME_FORMAT = "%Y-%m-%dT%H:%M:%SZ"
"""Standard datetime format (ISO 8601)."""


# =============================================================================
# Limits
# =============================================================================

MAX_STRING_LENGTH = 10000
"""Maximum allowed string length for user input."""

MAX_ARRAY_LENGTH = 1000
"""Maximum allowed array length for user input."""

MAX_FILE_SIZE_BYTES = 10 * 1024 * 1024  # 10 MB
"""Maximum allowed file upload size."""
