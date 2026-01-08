"""
Health Check Schemas.

Pydantic models for health check endpoint responses.
"""

from pydantic import BaseModel, Field


class HealthResponse(BaseModel):
    """
    Basic health check response.

    Attributes
    ----------
    status : str
        Health status (e.g., "healthy", "alive")
    service : str
        Name of the service
    version : str
        Version of the service
    """

    status: str = Field(..., description="Health status", examples=["healthy"])
    service: str = Field(..., description="Service name", examples=["my-api"])
    version: str = Field(..., description="Service version", examples=["0.1.0"])


class ReadinessResponse(BaseModel):
    """
    Readiness check response with dependency status.

    Attributes
    ----------
    status : str
        Overall readiness status ("ready" or "not_ready")
    checks : dict
        Individual dependency check results
    """

    status: str = Field(..., description="Readiness status", examples=["ready"])
    checks: dict[str, bool] = Field(
        default_factory=dict,
        description="Individual dependency checks",
        examples=[{"database": True, "redis": True}],
    )
