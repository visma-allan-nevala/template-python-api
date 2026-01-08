# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Quick Reference (for LLM agents)

**Start here for context:**
- `docs/ARCHITECTURE.md` - System design, layers, data flow
- `docs/DEVELOPMENT.md` - Setup guide, commands, adding features
- `docs/API.md` - API endpoint documentation (create as needed)
- `docs/SECURITY.md` - Security documentation (create as needed)

**When you need to find:**
| Looking for... | Go to... |
|----------------|----------|
| Entry point / main app | `src/api/main.py` |
| API routes | `src/api/routes/*.py` |
| Request/response schemas | `src/api/schemas/*.py` |
| Middleware (auth, logging, rate-limit) | `src/api/middleware/` |
| Configuration | `src/core/config.py` |
| Constants and enums | `src/core/constants.py` |
| Custom exceptions | `src/core/exceptions.py` |
| Database models | `src/models/` |
| Business logic services | `src/services/` |
| Database/cache clients | `src/storage/` |
| External service adapters | `src/adapters/` |
| Test fixtures | `tests/conftest.py` |

**Key patterns:**
- **Layered architecture**: API → Services → Storage/Adapters
- **Pydantic Settings**: Environment-based configuration in `src/core/config.py`
- **Async everywhere**: All I/O operations should be async
- **Type hints**: Strict mypy checking enabled
- **Repository pattern**: Data access through repository classes in `src/storage/`
- **Adapter pattern**: External API integrations through adapters in `src/adapters/`

**Common tasks:**
- Add new API endpoint: Create route in `src/api/routes/`, add schema in `src/api/schemas/`
- Add new service: Create class in `src/services/`, inject via FastAPI Depends()
- Add new model: Create in `src/models/`, run migration
- Add external integration: Create adapter in `src/adapters/`, inject via FastAPI Depends()
- Add configuration: Add to `src/core/config.py`, document in `.env.example`

## Commands

**Prerequisites:** Python 3.12+, [uv](https://docs.astral.sh/uv/) package manager

```bash
# Initial setup (run once after clone)
./setup.sh            # or: make setup

# Install dependencies
uv sync
uv sync --extra dev   # Include development dependencies
uv sync --extra db    # Include database dependencies
uv sync --extra redis # Include Redis dependencies

# Run development server
make dev              # or: uv run uvicorn src.api.main:app --reload

# Run tests
make test             # Run all tests
make test-v           # Run tests with verbose output
make test-cov         # Run with coverage report
make test-unit        # Run only unit tests

# Code quality
make check            # Run all checks (lint, typecheck)
make lint-fix         # Auto-fix lint issues
make format           # Format code with ruff

# Docker
make docker-up        # Start services (PostgreSQL, Redis)
make docker-down      # Stop services

# Pre-commit hooks
make pre-commit       # Run all hooks manually
```

## Architecture

```
HTTP Request
     │
     ▼
┌─────────────────────────────────────────────────────────────────┐
│                        API Layer (FastAPI)                       │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐             │
│  │   Routes    │  │  Schemas    │  │ Middleware  │             │
│  │ /health     │  │ Pydantic    │  │ Auth, Log   │             │
│  └─────────────┘  └─────────────┘  └─────────────┘             │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                      Service Layer                               │
│  Business logic, orchestration, validation                      │
└────────────────────────────┬────────────────────────────────────┘
                             │
              ┌──────────────┴──────────────┐
              ▼                             ▼
┌────────────────────────────┐  ┌────────────────────────────────┐
│       Storage Layer        │  │        Adapters Layer          │
│  ┌──────────┐ ┌──────────┐ │  │  ┌──────────────────────────┐  │
│  │ Database │ │  Redis   │ │  │  │   External API Clients   │  │
│  │ (Postgres)│ │ (Cache)  │ │  │  │  (HTTP, gRPC, etc.)      │  │
│  └──────────┘ └──────────┘ │  │  └──────────────────────────┘  │
└────────────────────────────┘  └────────────────────────────────┘
```

## Code Organization

```
src/
├── api/                    # FastAPI application
│   ├── main.py            # App entry point
│   ├── routes/            # API endpoints
│   ├── schemas/           # Pydantic models
│   └── middleware/        # Auth, logging, rate limiting
├── adapters/              # External service integrations
│   └── (api_client.py)    # HTTP/gRPC clients for external APIs
├── core/                  # Configuration and utilities
│   ├── config.py          # Settings management
│   ├── constants.py       # Constants and enums
│   └── exceptions.py      # Custom exceptions
├── models/                # Database models (SQLAlchemy)
├── services/              # Business logic
├── storage/               # Data access layer
│   ├── database.py        # PostgreSQL connection
│   └── redis_client.py    # Redis connection
└── utils/                 # Helper functions
```

## Environment Variables

Key environment variables (see `.env.example` for all):

| Variable | Description | Default |
|----------|-------------|---------|
| `APP_NAME` | Application name | `my-api` |
| `APP_ENV` | Environment (local/dev/staging/prod) | `local` |
| `DEBUG` | Enable debug mode | `false` |
| `DATABASE_HOST` | PostgreSQL host | `localhost` |
| `DATABASE_PORT` | PostgreSQL port | `5432` |
| `REDIS_HOST` | Redis host | `localhost` |
| `API_KEYS` | Comma-separated API keys | - |

## Git Commit Guidelines

Do not include "Claude", "Co-Authored-By", or any AI assistant attribution in commit messages.

## Code Review Agents

The `.claude/agents/` folder contains LLM agent prompts for code review. See `.claude/agents/README.md` for usage.

Before committing:
```
Review Mode: changed
Agents: software_architect, cybersecurity_engineer, qa_test_engineer
```
