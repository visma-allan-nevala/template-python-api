"""
Custom Exception Classes.

Domain-specific exceptions for consistent error handling across the application.
All exceptions inherit from `APIError` for unified handling in FastAPI.

Usage
-----
Raise exceptions in services::

    from src.core.exceptions import NotFoundError, ValidationError

    def get_user(user_id: str) -> User:
        user = db.get(user_id)
        if not user:
            raise NotFoundError("User", user_id)
        return user

    def create_user(data: dict) -> User:
        if not data.get("email"):
            raise ValidationError("email", "Email is required")
        ...

The exception handler in `main.py` converts these to JSON responses::

    {
        "error": {
            "code": "NOT_FOUND",
            "message": "User with ID '123' not found",
            "details": {"entity": "User", "id": "123"}
        }
    }

Exception Hierarchy
-------------------
APIError (base)
├── ValidationError (400)
├── AuthenticationError (401)
├── AuthorizationError (403)
├── NotFoundError (404)
├── ConflictError (409)
├── RateLimitError (429)
└── ExternalServiceError (502/503)
"""

from typing import Any


class APIError(Exception):
    """
    Base exception for all API errors.

    All custom exceptions should inherit from this class to ensure
    consistent error handling and response formatting.

    Parameters
    ----------
    message : str
        Human-readable error message
    error_code : str
        Machine-readable error code (e.g., "NOT_FOUND")
    status_code : int
        HTTP status code
    details : dict | None
        Additional error details
    """

    def __init__(
        self,
        message: str,
        error_code: str = "INTERNAL_ERROR",
        status_code: int = 500,
        details: dict[str, Any] | None = None,
    ) -> None:
        super().__init__(message)
        self.message = message
        self.error_code = error_code
        self.status_code = status_code
        self.details = details or {}

    def __str__(self) -> str:
        return f"{self.error_code}: {self.message}"


class ValidationError(APIError):
    """
    Validation error (400 Bad Request).

    Raised when request data fails validation.

    Parameters
    ----------
    field : str
        Name of the invalid field
    message : str
        Description of the validation failure
    """

    def __init__(self, field: str, message: str) -> None:
        super().__init__(
            message=f"Validation error on field '{field}': {message}",
            error_code="VALIDATION_ERROR",
            status_code=400,
            details={"field": field, "reason": message},
        )


class AuthenticationError(APIError):
    """
    Authentication error (401 Unauthorized).

    Raised when authentication fails or credentials are missing.
    """

    def __init__(self, message: str = "Authentication required") -> None:
        super().__init__(
            message=message,
            error_code="UNAUTHORIZED",
            status_code=401,
        )


class AuthorizationError(APIError):
    """
    Authorization error (403 Forbidden).

    Raised when user lacks permission for the requested action.
    """

    def __init__(
        self, message: str = "Permission denied", resource: str | None = None
    ) -> None:
        super().__init__(
            message=message,
            error_code="FORBIDDEN",
            status_code=403,
            details={"resource": resource} if resource else {},
        )


class NotFoundError(APIError):
    """
    Resource not found error (404 Not Found).

    Raised when a requested resource does not exist.

    Parameters
    ----------
    entity : str
        Type of entity (e.g., "User", "Order")
    identifier : str
        ID or identifier of the missing entity
    """

    def __init__(self, entity: str, identifier: str) -> None:
        super().__init__(
            message=f"{entity} with ID '{identifier}' not found",
            error_code="NOT_FOUND",
            status_code=404,
            details={"entity": entity, "id": identifier},
        )


class ConflictError(APIError):
    """
    Conflict error (409 Conflict).

    Raised when the request conflicts with current state
    (e.g., duplicate entry, version mismatch).
    """

    def __init__(self, message: str, details: dict[str, Any] | None = None) -> None:
        super().__init__(
            message=message,
            error_code="CONFLICT",
            status_code=409,
            details=details or {},
        )


class RateLimitError(APIError):
    """
    Rate limit exceeded (429 Too Many Requests).

    Raised when client exceeds rate limits.
    """

    def __init__(
        self,
        message: str = "Rate limit exceeded",
        retry_after: int | None = None,
    ) -> None:
        details = {}
        if retry_after:
            details["retry_after_seconds"] = retry_after
        super().__init__(
            message=message,
            error_code="RATE_LIMITED",
            status_code=429,
            details=details,
        )


class ExternalServiceError(APIError):
    """
    External service error (502/503).

    Raised when an external service call fails.

    Parameters
    ----------
    service : str
        Name of the external service
    message : str
        Error description
    """

    def __init__(self, service: str, message: str) -> None:
        super().__init__(
            message=f"External service '{service}' error: {message}",
            error_code="SERVICE_UNAVAILABLE",
            status_code=503,
            details={"service": service},
        )


class DatabaseError(APIError):
    """
    Database operation error (500).

    Raised when a database operation fails unexpectedly.
    """

    def __init__(self, operation: str, message: str) -> None:
        super().__init__(
            message=f"Database error during {operation}: {message}",
            error_code="DATABASE_ERROR",
            status_code=500,
            details={"operation": operation},
        )
