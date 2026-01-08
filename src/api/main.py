"""
FastAPI Application Entry Point.

This module initializes and configures the FastAPI application instance.
It sets up lifecycle events, middleware, exception handlers, and routes.

Usage
-----
Run with uvicorn:

    uvicorn src.api.main:app --reload --host 0.0.0.0 --port 8000

Or via Makefile:

    make dev
"""

from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from src.api.routes import health
from src.core.config import settings
from src.core.exceptions import APIError


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """
    Application lifespan context manager.

    Handles startup and shutdown events for the application.
    Use this for initializing and cleaning up resources like:
    - Database connection pools
    - Cache connections
    - Background task schedulers

    Example
    -------
    Add startup initialization::

        # Startup
        app.state.db = await create_database_pool()
        app.state.redis = await create_redis_client()

        yield  # Application runs here

        # Shutdown
        await app.state.db.close()
        await app.state.redis.close()
    """
    # === Startup ===
    # TODO: Initialize database connections
    # TODO: Initialize cache connections
    # TODO: Start background tasks

    yield

    # === Shutdown ===
    # TODO: Close database connections
    # TODO: Close cache connections
    # TODO: Stop background tasks


def create_application() -> FastAPI:
    """
    Create and configure the FastAPI application.

    This factory function allows for easy testing by creating
    fresh app instances with different configurations.

    Returns
    -------
    FastAPI
        Configured FastAPI application instance.
    """
    app = FastAPI(
        title=settings.app_name,
        description="A FastAPI application",
        version="0.1.0",
        docs_url="/docs" if settings.debug else None,
        redoc_url="/redoc" if settings.debug else None,
        openapi_url="/openapi.json" if settings.debug else None,
        lifespan=lifespan,
    )

    # =========================================================================
    # Middleware
    # =========================================================================

    # CORS middleware
    if settings.cors_origins:
        app.add_middleware(
            CORSMiddleware,
            allow_origins=settings.cors_origins,
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )

    # TODO: Add authentication middleware
    # from src.api.middleware.auth import AuthMiddleware
    # app.add_middleware(AuthMiddleware)

    # TODO: Add request logging middleware
    # from src.api.middleware.logging import LoggingMiddleware
    # app.add_middleware(LoggingMiddleware)

    # TODO: Add rate limiting middleware
    # from src.api.middleware.rate_limit import RateLimitMiddleware
    # app.add_middleware(RateLimitMiddleware)

    # =========================================================================
    # Exception Handlers
    # =========================================================================

    @app.exception_handler(APIError)
    async def api_error_handler(request: Request, exc: APIError) -> JSONResponse:
        """Handle custom API errors."""
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "error": {
                    "code": exc.error_code,
                    "message": exc.message,
                    "details": exc.details,
                }
            },
        )

    @app.exception_handler(Exception)
    async def generic_exception_handler(request: Request, exc: Exception) -> JSONResponse:
        """Handle unexpected exceptions."""
        # Log the error for debugging
        # logger.exception("Unexpected error", exc_info=exc)

        # Return generic error in production
        if not settings.debug:
            return JSONResponse(
                status_code=500,
                content={
                    "error": {
                        "code": "INTERNAL_ERROR",
                        "message": "An unexpected error occurred",
                    }
                },
            )

        # Return detailed error in debug mode
        return JSONResponse(
            status_code=500,
            content={
                "error": {
                    "code": "INTERNAL_ERROR",
                    "message": str(exc),
                    "type": type(exc).__name__,
                }
            },
        )

    # =========================================================================
    # Routes
    # =========================================================================

    # Include routers
    app.include_router(health.router, prefix="/api/v1")

    # TODO: Add your route modules here
    # from src.api.routes import users, items
    # app.include_router(users.router, prefix="/api/v1")
    # app.include_router(items.router, prefix="/api/v1")

    return app


# Create the application instance
app = create_application()
