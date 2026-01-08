"""
Request/Response Logging Middleware.

Logs request details and response times for monitoring, debugging, and auditing.

Usage
-----
Add to your FastAPI app in `main.py`::

    from src.api.middleware.logging import LoggingMiddleware
    app.add_middleware(LoggingMiddleware)

Log Output
----------
Each request logs:
- Request: method, path, client IP, user agent
- Response: status code, duration in milliseconds

Example log output::

    INFO: GET /api/v1/health - 200 OK - 5.23ms
    INFO: POST /api/v1/users - 201 Created - 45.12ms - user_id=123
    WARNING: GET /api/v1/users/456 - 404 Not Found - 12.34ms

Configuration
-------------
Set `LOG_LEVEL` environment variable to control verbosity:
- DEBUG: Log request/response bodies (careful with sensitive data)
- INFO: Log request summaries (default)
- WARNING: Log only errors and slow requests
"""

import logging
import time
from collections.abc import Awaitable, Callable
from typing import Any

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response

logger = logging.getLogger(__name__)


class LoggingMiddleware(BaseHTTPMiddleware):
    """
    Middleware for logging HTTP requests and responses.

    Logs request details including method, path, status code, and duration.
    Can be extended to log request/response bodies for debugging.
    """

    async def dispatch(
        self, request: Request, call_next: Callable[[Request], Awaitable[Response]]
    ) -> Response:
        """
        Process request and log details.

        Parameters
        ----------
        request : Request
            Incoming HTTP request
        call_next : Callable
            Next middleware or route handler

        Returns
        -------
        Response
            HTTP response
        """
        # Extract request info
        request_id = request.headers.get("X-Request-ID", "-")
        client_ip = self._get_client_ip(request)
        method = request.method
        path = request.url.path
        query = str(request.query_params) if request.query_params else ""

        # Start timer
        start_time = time.perf_counter()

        # Process request
        try:
            response = await call_next(request)

            # Calculate duration
            duration_ms = (time.perf_counter() - start_time) * 1000

            # Log based on status code
            status_code = response.status_code
            log_data = self._build_log_data(
                request_id=request_id,
                client_ip=client_ip,
                method=method,
                path=path,
                query=query,
                status_code=status_code,
                duration_ms=duration_ms,
            )

            if status_code >= 500:
                logger.error("Request failed", extra=log_data)
            elif status_code >= 400:
                logger.warning("Request error", extra=log_data)
            else:
                logger.info("Request completed", extra=log_data)

            # Add response headers
            response.headers["X-Request-ID"] = request_id
            response.headers["X-Response-Time"] = f"{duration_ms:.2f}ms"

            return response

        except Exception as e:
            # Log exception
            duration_ms = (time.perf_counter() - start_time) * 1000
            logger.exception(
                "Request exception",
                extra={
                    "request_id": request_id,
                    "client_ip": client_ip,
                    "method": method,
                    "path": path,
                    "duration_ms": duration_ms,
                    "error": str(e),
                },
            )
            raise

    def _get_client_ip(self, request: Request) -> str:
        """Extract client IP from request headers or connection."""
        # Check X-Forwarded-For for reverse proxy setups
        forwarded_for = request.headers.get("X-Forwarded-For")
        if forwarded_for:
            return forwarded_for.split(",")[0].strip()

        # Check X-Real-IP
        real_ip = request.headers.get("X-Real-IP")
        if real_ip:
            return real_ip

        # Fall back to direct connection
        if request.client:
            return request.client.host

        return "unknown"

    def _build_log_data(
        self,
        request_id: str,
        client_ip: str,
        method: str,
        path: str,
        query: str,
        status_code: int,
        duration_ms: float,
    ) -> dict[str, Any]:
        """Build structured log data."""
        return {
            "request_id": request_id,
            "client_ip": client_ip,
            "method": method,
            "path": path,
            "query": query,
            "status_code": status_code,
            "duration_ms": round(duration_ms, 2),
        }
