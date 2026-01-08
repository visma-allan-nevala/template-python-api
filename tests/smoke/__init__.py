"""
Smoke Tests.

Quick verification tests for deployed environments.
These tests verify basic functionality is working after deployment.

Run smoke tests:
    make test-smoke
    uv run pytest tests/smoke -v

Usage for deployed environments:
    API_BASE_URL=https://api.example.com uv run pytest tests/smoke -v
"""
