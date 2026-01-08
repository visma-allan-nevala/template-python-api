"""
Smoke Test Configuration.

Fixtures specific to smoke tests against deployed environments.
"""

import os

import httpx
import pytest


@pytest.fixture
def base_url() -> str:
    """
    Get the base URL for smoke tests.

    Set API_BASE_URL environment variable to test deployed environments.
    Defaults to localhost for local testing.
    """
    return os.environ.get("API_BASE_URL", "http://localhost:8000")


@pytest.fixture
def api_client(base_url: str) -> httpx.Client:
    """
    HTTP client for smoke tests.

    Uses synchronous httpx client for deployed environment testing.
    """
    return httpx.Client(base_url=base_url, timeout=30.0)


@pytest.fixture
def api_key() -> str | None:
    """
    API key for authenticated smoke tests.

    Set API_KEY environment variable for testing protected endpoints.
    """
    return os.environ.get("API_KEY")


@pytest.fixture
def auth_headers(api_key: str | None) -> dict[str, str]:
    """Headers with API key if available."""
    if api_key:
        return {"X-API-Key": api_key}
    return {}
