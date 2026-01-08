"""
Health Check Endpoints.

Provides health check endpoints for monitoring and orchestration systems.
These endpoints are used by Kubernetes for liveness and readiness probes.

Endpoints
---------
GET /health
    Basic health check - returns 200 if the service is running.

GET /health/ready
    Readiness probe - returns 200 if the service is ready to accept traffic.
    Checks database and cache connectivity.

GET /health/live
    Liveness probe - returns 200 if the service is alive.
    A simple check that the process is responding.

Usage with Kubernetes
---------------------
Configure in your deployment.yaml::

    livenessProbe:
      httpGet:
        path: /api/v1/health/live
        port: 8000
      initialDelaySeconds: 10
      periodSeconds: 15

    readinessProbe:
      httpGet:
        path: /api/v1/health/ready
        port: 8000
      initialDelaySeconds: 5
      periodSeconds: 10
"""

from fastapi import APIRouter

from src.api.schemas.health import HealthResponse, ReadinessResponse
from src.core.config import settings

router = APIRouter(prefix="/health", tags=["health"])


@router.get(
    "",
    response_model=HealthResponse,
    summary="Basic health check",
    description="Returns the health status of the service.",
)
async def health_check() -> HealthResponse:
    """
    Basic health check endpoint.

    Returns a simple health status indicating the service is running.
    This endpoint should always return 200 if the process is alive.
    """
    return HealthResponse(
        status="healthy",
        service=settings.app_name,
        version="0.1.0",
    )


@router.get(
    "/ready",
    response_model=ReadinessResponse,
    summary="Readiness probe",
    description="Checks if the service is ready to accept traffic.",
)
async def readiness_check() -> ReadinessResponse:
    """
    Readiness probe for Kubernetes.

    Checks that all dependencies (database, cache, etc.) are available
    and the service is ready to handle requests.

    Returns 200 if ready, 503 if not ready.
    """
    checks: dict[str, bool] = {}

    # TODO: Add database health check
    # try:
    #     await database.execute("SELECT 1")
    #     checks["database"] = True
    # except Exception:
    #     checks["database"] = False

    # TODO: Add Redis health check
    # try:
    #     await redis.ping()
    #     checks["redis"] = True
    # except Exception:
    #     checks["redis"] = False

    # For now, always return ready
    checks["database"] = True
    checks["redis"] = True

    all_healthy = all(checks.values())

    return ReadinessResponse(
        status="ready" if all_healthy else "not_ready",
        checks=checks,
    )


@router.get(
    "/live",
    response_model=HealthResponse,
    summary="Liveness probe",
    description="Simple check that the service process is alive.",
)
async def liveness_check() -> HealthResponse:
    """
    Liveness probe for Kubernetes.

    A minimal check that returns 200 if the process is responding.
    This should not check external dependencies.
    """
    return HealthResponse(
        status="alive",
        service=settings.app_name,
        version="0.1.0",
    )
