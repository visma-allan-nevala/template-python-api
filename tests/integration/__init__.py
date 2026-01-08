"""
Integration Tests.

Tests that require external dependencies like databases, caches,
or external APIs. These tests are slower but verify real integration.

Run integration tests only:
    make test-integration
    uv run pytest tests/integration -v

Prerequisites:
- Docker services running: make docker-up
- Or use test containers (automatically managed)
"""
