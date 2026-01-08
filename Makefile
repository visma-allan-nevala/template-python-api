# =============================================================================
# Makefile for FastAPI Application
# =============================================================================
# Run `make help` to see available commands
# =============================================================================

.PHONY: help setup dev test test-v test-cov test-fast check lint lint-fix format typecheck \
        docker-up docker-down docker-build docker-logs clean quick-check ci

# Default target
.DEFAULT_GOAL := help

# Colors for terminal output
BLUE := \033[34m
GREEN := \033[32m
YELLOW := \033[33m
RESET := \033[0m

# =============================================================================
# Help
# =============================================================================

help: ## Show this help message
	@echo "$(BLUE)FastAPI Template - Available Commands$(RESET)"
	@echo ""
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | \
		awk 'BEGIN {FS = ":.*?## "}; {printf "  $(GREEN)%-15s$(RESET) %s\n", $$1, $$2}'
	@echo ""

# =============================================================================
# Setup
# =============================================================================

setup: ## Initial setup: install deps and pre-commit hooks
	@echo "$(BLUE)Installing dependencies...$(RESET)"
	uv sync --extra dev
	@echo "$(BLUE)Installing pre-commit hooks...$(RESET)"
	uv run pre-commit install
	uv run pre-commit install --hook-type pre-push
	@echo "$(GREEN)Setup complete!$(RESET)"

# =============================================================================
# Development
# =============================================================================

dev: ## Run development server with hot reload
	uv run uvicorn src.api.main:app --reload --host 0.0.0.0 --port 8000

run: ## Run production server
	uv run uvicorn src.api.main:app --host 0.0.0.0 --port 8000

# =============================================================================
# Testing
# =============================================================================

test: ## Run all tests
	uv run pytest

test-v: ## Run tests with verbose output
	uv run pytest -v

test-cov: ## Run tests with coverage report
	uv run pytest --cov=src --cov-report=html --cov-report=term-missing
	@echo "$(GREEN)Coverage report: htmlcov/index.html$(RESET)"

test-fast: ## Run tests in parallel (faster)
	uv run pytest -n auto

test-unit: ## Run only unit tests
	uv run pytest tests/unit -v

test-integration: ## Run only integration tests
	uv run pytest tests/integration -v

test-smoke: ## Run only smoke tests
	uv run pytest tests/smoke -v

test-failed: ## Re-run only failed tests
	uv run pytest --lf

# =============================================================================
# Code Quality
# =============================================================================

check: lint typecheck ## Run all checks (lint + typecheck)
	@echo "$(GREEN)All checks passed!$(RESET)"

lint: ## Run linter (ruff)
	uv run ruff check src/ tests/

lint-fix: ## Auto-fix lint issues
	uv run ruff check src/ tests/ --fix
	uv run ruff format src/ tests/

format: ## Format code with ruff
	uv run ruff format src/ tests/

typecheck: ## Run type checker (mypy)
	uv run mypy src/

pre-commit: ## Run pre-commit on all files
	uv run pre-commit run --all-files

# =============================================================================
# Docker
# =============================================================================

docker-up: ## Start all Docker services
	docker-compose up -d

docker-down: ## Stop all Docker services
	docker-compose down

docker-build: ## Build Docker image
	docker build -t my-api .

docker-logs: ## View Docker logs
	docker-compose logs -f

docker-ps: ## List running containers
	docker-compose ps

docker-clean: ## Stop services and remove volumes
	docker-compose down -v

# =============================================================================
# Database (uncomment when using Alembic)
# =============================================================================

# migrate: ## Run database migrations
# 	uv run alembic upgrade head

# migrate-create: ## Create a new migration (usage: make migrate-create MSG="description")
# 	uv run alembic revision --autogenerate -m "$(MSG)"

# migrate-down: ## Rollback last migration
# 	uv run alembic downgrade -1

# =============================================================================
# Cleanup
# =============================================================================

clean: ## Remove build artifacts and caches
	rm -rf .pytest_cache/
	rm -rf .ruff_cache/
	rm -rf .mypy_cache/
	rm -rf htmlcov/
	rm -rf .coverage
	rm -rf dist/
	rm -rf build/
	rm -rf *.egg-info/
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete 2>/dev/null || true
	@echo "$(GREEN)Cleaned!$(RESET)"

# =============================================================================
# CI Helpers
# =============================================================================

quick-check: lint-fix test ## Quick check: fix lint issues and run tests

ci: check test-cov ## Full CI pipeline: all checks + tests with coverage
