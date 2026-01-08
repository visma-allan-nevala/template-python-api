"""
Pytest Configuration and Fixtures.

This module contains shared fixtures used across all test modules.
Fixtures provide test dependencies like clients, mocks, and test data.

Usage
-----
Fixtures are automatically discovered by pytest. Use them as parameters::

    def test_health_check(client):
        response = client.get("/api/v1/health")
        assert response.status_code == 200

Available Fixtures
------------------
client : TestClient
    Synchronous test client for FastAPI app

async_client : AsyncClient
    Asynchronous test client for async tests

mock_settings : Settings
    Settings with test overrides

sample_user : dict
    Sample user data for tests

Adding Fixtures
---------------
Add reusable fixtures here. For test-specific fixtures,
add them to the test module or a conftest.py in the subdirectory.
"""

from collections.abc import AsyncGenerator, Generator
from typing import Any
from unittest.mock import patch

import pytest
from fastapi.testclient import TestClient
from httpx import ASGITransport, AsyncClient

from src.api.main import app
from src.core.config import Settings


@pytest.fixture
def client() -> Generator[TestClient, None, None]:
    """
    Synchronous test client for FastAPI app.

    Use for testing endpoints that don't require async operations.

    Example
    -------
    ::

        def test_health(client):
            response = client.get("/api/v1/health")
            assert response.status_code == 200
    """
    with TestClient(app) as test_client:
        yield test_client


@pytest.fixture
async def async_client() -> AsyncGenerator[AsyncClient, None]:
    """
    Asynchronous test client for FastAPI app.

    Use for testing async endpoints or when you need async setup.

    Example
    -------
    ::

        @pytest.mark.asyncio
        async def test_async_endpoint(async_client):
            response = await async_client.get("/api/v1/health")
            assert response.status_code == 200
    """
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        yield client


@pytest.fixture
def mock_settings() -> Generator[Settings, None, None]:
    """
    Settings with test overrides.

    Provides a Settings instance configured for testing.
    Patches the settings singleton for the duration of the test.

    Example
    -------
    ::

        def test_with_mock_settings(mock_settings):
            assert mock_settings.debug is True
    """
    test_settings = Settings(
        app_name="test-api",
        app_env="test",
        debug=True,
        api_keys=["test-api-key"],
        secret_key="test-secret-key",
    )

    with patch("src.core.config.settings", test_settings):
        yield test_settings


@pytest.fixture
def auth_headers() -> dict[str, str]:
    """
    Authentication headers with test API key.

    Use for testing protected endpoints.

    Example
    -------
    ::

        def test_protected_endpoint(client, auth_headers):
            response = client.get("/api/v1/protected", headers=auth_headers)
            assert response.status_code == 200
    """
    return {"X-API-Key": "test-api-key"}


@pytest.fixture
def sample_user() -> dict[str, Any]:
    """
    Sample user data for tests.

    Returns
    -------
    dict
        User data dictionary
    """
    return {
        "id": "user-123",
        "email": "test@example.com",
        "name": "Test User",
        "is_active": True,
    }


@pytest.fixture
def sample_users() -> list[dict[str, Any]]:
    """
    List of sample users for tests.

    Returns
    -------
    list[dict]
        List of user data dictionaries
    """
    return [
        {"id": "user-1", "email": "user1@example.com", "name": "User One"},
        {"id": "user-2", "email": "user2@example.com", "name": "User Two"},
        {"id": "user-3", "email": "user3@example.com", "name": "User Three"},
    ]


# =============================================================================
# Database Fixtures (uncomment when using database)
# =============================================================================

# @pytest.fixture
# async def db_session() -> AsyncGenerator[AsyncSession, None]:
#     """Database session for tests with automatic rollback."""
#     from src.storage.database import get_session_factory
#
#     factory = get_session_factory()
#     async with factory() as session:
#         yield session
#         await session.rollback()


# =============================================================================
# Redis Fixtures (uncomment when using Redis)
# =============================================================================

# @pytest.fixture
# async def redis_client() -> AsyncGenerator[Redis, None]:
#     """Redis client for tests."""
#     from src.storage.redis_client import get_redis_client
#
#     client = await get_redis_client()
#     yield client
#     # Clean up test keys
#     await client.flushdb()
