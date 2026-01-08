"""
Rate Limiting Middleware.

Prevents abuse by limiting the number of requests per client/IP within a time window.

Usage
-----
Add to your FastAPI app in `main.py`::

    from src.api.middleware.rate_limit import RateLimitMiddleware
    app.add_middleware(RateLimitMiddleware, requests_per_minute=100)

Or use as a dependency for specific routes::

    from src.api.middleware.rate_limit import rate_limit

    @router.get("/expensive-operation")
    async def expensive_route(_: None = Depends(rate_limit(requests=10, window=60))):
        return {"result": "..."}

Configuration
-------------
Environment variables:
- `RATE_LIMIT_ENABLED`: Enable/disable rate limiting (default: false)
- `RATE_LIMIT_REQUESTS`: Max requests per window (default: 100)
- `RATE_LIMIT_WINDOW_SECONDS`: Time window in seconds (default: 60)

Response Headers
----------------
Rate limit info is returned in response headers:
- `X-RateLimit-Limit`: Maximum requests allowed
- `X-RateLimit-Remaining`: Requests remaining in window
- `X-RateLimit-Reset`: Unix timestamp when window resets

When rate limited, returns 429 Too Many Requests.

Storage Backends
----------------
This implementation uses in-memory storage (suitable for single-instance).
For multi-instance deployments, use Redis backend (implementation provided).
"""

import time
from collections import defaultdict
from collections.abc import Awaitable, Callable
from typing import Any

from fastapi import Depends, HTTPException, Request, status
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response

# In-memory store (for single instance)
# For production, use Redis or similar
_request_counts: dict[str, list[float]] = defaultdict(list)


class RateLimitMiddleware(BaseHTTPMiddleware):
    """
    Rate limiting middleware using sliding window algorithm.

    Parameters
    ----------
    app : ASGIApp
        The ASGI application
    requests_per_minute : int
        Maximum requests per minute (default: 100)
    """

    def __init__(self, app: Any, requests_per_minute: int = 100) -> None:
        super().__init__(app)
        self.max_requests = requests_per_minute
        self.window_seconds = 60

    async def dispatch(
        self, request: Request, call_next: Callable[[Request], Awaitable[Response]]
    ) -> Response:
        """
        Check rate limit and process request.

        Parameters
        ----------
        request : Request
            Incoming HTTP request
        call_next : Callable
            Next middleware or route handler

        Returns
        -------
        Response
            HTTP response with rate limit headers
        """
        # Get client identifier (IP or API key)
        client_id = self._get_client_id(request)

        # Check rate limit
        current_time = time.time()
        window_start = current_time - self.window_seconds

        # Clean old requests and count recent ones
        _request_counts[client_id] = [
            t for t in _request_counts[client_id] if t > window_start
        ]
        request_count = len(_request_counts[client_id])

        # Calculate remaining requests and reset time
        remaining = max(0, self.max_requests - request_count - 1)
        reset_time = int(window_start + self.window_seconds)

        # Add rate limit headers
        headers = {
            "X-RateLimit-Limit": str(self.max_requests),
            "X-RateLimit-Remaining": str(remaining),
            "X-RateLimit-Reset": str(reset_time),
        }

        # Check if over limit
        if request_count >= self.max_requests:
            return Response(
                content='{"error": {"code": "RATE_LIMITED", "message": "Too many requests"}}',
                status_code=429,
                headers=headers,
                media_type="application/json",
            )

        # Record this request
        _request_counts[client_id].append(current_time)

        # Process request
        response = await call_next(request)

        # Add rate limit headers to response
        for key, value in headers.items():
            response.headers[key] = value

        return response

    def _get_client_id(self, request: Request) -> str:
        """
        Get unique client identifier.

        Uses API key if present, otherwise falls back to IP address.
        """
        # Check for API key
        api_key = request.headers.get("X-API-Key")
        if api_key:
            return f"key:{api_key[:16]}"

        # Fall back to IP
        forwarded = request.headers.get("X-Forwarded-For")
        if forwarded:
            return f"ip:{forwarded.split(',')[0].strip()}"

        if request.client:
            return f"ip:{request.client.host}"

        return "ip:unknown"


def rate_limit(requests: int = 10, window: int = 60) -> Callable[..., None]:
    """
    Dependency for per-route rate limiting.

    Parameters
    ----------
    requests : int
        Maximum requests per window
    window : int
        Time window in seconds

    Returns
    -------
    Callable
        FastAPI dependency

    Example
    -------
    ::

        @router.post("/expensive")
        async def expensive_operation(
            _: None = Depends(rate_limit(requests=5, window=60))
        ):
            return {"result": "..."}
    """
    async def _rate_limit_dependency(request: Request) -> None:
        client_ip = request.client.host if request.client else "unknown"
        key = f"route:{request.url.path}:{client_ip}"

        current_time = time.time()
        window_start = current_time - window

        # Clean and count
        _request_counts[key] = [t for t in _request_counts[key] if t > window_start]

        if len(_request_counts[key]) >= requests:
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail="Rate limit exceeded for this endpoint",
            )

        _request_counts[key].append(current_time)

    return Depends(_rate_limit_dependency)


# Redis-based rate limiter for production (uncomment to use)
#
# import redis.asyncio as redis
#
# class RedisRateLimiter:
#     def __init__(self, redis_client: redis.Redis, max_requests: int, window: int):
#         self.redis = redis_client
#         self.max_requests = max_requests
#         self.window = window
#
#     async def is_allowed(self, key: str) -> tuple[bool, int, int]:
#         """Check if request is allowed and return (allowed, remaining, reset_at)."""
#         current = int(time.time())
#         window_key = f"ratelimit:{key}:{current // self.window}"
#
#         async with self.redis.pipeline() as pipe:
#             pipe.incr(window_key)
#             pipe.expire(window_key, self.window)
#             results = await pipe.execute()
#
#         count = results[0]
#         remaining = max(0, self.max_requests - count)
#         reset_at = (current // self.window + 1) * self.window
#
#         return count <= self.max_requests, remaining, reset_at
