"""
Tests for Health Check Endpoints.

These tests verify the health check endpoints work correctly
for Kubernetes liveness and readiness probes.
"""

import pytest
from fastapi.testclient import TestClient


class TestHealthEndpoints:
    """Tests for /api/v1/health endpoints."""

    def test_health_check(self, client: TestClient) -> None:
        """Test basic health check returns 200."""
        response = client.get("/api/v1/health")

        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert "service" in data
        assert "version" in data

    def test_liveness_probe(self, client: TestClient) -> None:
        """Test liveness probe returns 200."""
        response = client.get("/api/v1/health/live")

        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "alive"

    def test_readiness_probe(self, client: TestClient) -> None:
        """Test readiness probe returns 200 when healthy."""
        response = client.get("/api/v1/health/ready")

        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "ready"
        assert "checks" in data

    def test_health_response_format(self, client: TestClient) -> None:
        """Test health response has correct format."""
        response = client.get("/api/v1/health")

        assert response.status_code == 200
        data = response.json()

        # Verify required fields
        assert isinstance(data["status"], str)
        assert isinstance(data["service"], str)
        assert isinstance(data["version"], str)


class TestHealthAsync:
    """Async tests for health endpoints."""

    @pytest.mark.asyncio
    async def test_health_check_async(self, async_client) -> None:
        """Test health check with async client."""
        response = await async_client.get("/api/v1/health")

        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"

    @pytest.mark.asyncio
    async def test_readiness_async(self, async_client) -> None:
        """Test readiness probe with async client."""
        response = await async_client.get("/api/v1/health/ready")

        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "ready"
