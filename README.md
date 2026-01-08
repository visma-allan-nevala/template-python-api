# My API

A FastAPI application template for building production-ready REST APIs.

## Features

- **FastAPI** - Modern, fast web framework for building APIs
- **Async/Await** - Full async support for high performance
- **Type Safety** - Strict type checking with mypy
- **Auto Documentation** - OpenAPI/Swagger docs auto-generated
- **Docker Ready** - Multi-stage Dockerfile for production
- **CI/CD** - GitHub Actions workflows included
- **Code Quality** - Pre-commit hooks with ruff linting

## Quick Start

### Prerequisites

- Python 3.12+
- [uv](https://docs.astral.sh/uv/) package manager

### Setup

```bash
# Clone the repository
git clone https://github.com/your-org/my-api.git
cd my-api

# Run automated setup
./setup.sh

# Or manual setup:
uv sync --extra dev
uv run pre-commit install
cp .env.example .env
```

### Run Development Server

```bash
make dev
# or: uv run uvicorn src.api.main:app --reload
```

Visit:
- API: http://localhost:8000
- Docs: http://localhost:8000/docs
- Health: http://localhost:8000/api/v1/health

### Run Tests

```bash
make test          # Run all tests
make test-cov      # Run with coverage report
```

### Code Quality

```bash
make check         # Run linting and type checking
make lint-fix      # Auto-fix lint issues
```

## Project Structure

```
├── src/
│   ├── api/              # FastAPI application
│   │   ├── main.py       # App entry point
│   │   ├── routes/       # API endpoints
│   │   ├── schemas/      # Request/response models
│   │   └── middleware/   # Auth, logging, etc.
│   ├── core/             # Configuration, constants
│   ├── models/           # Database models
│   ├── services/         # Business logic
│   ├── storage/          # Data access layer
│   └── utils/            # Utilities
├── tests/                # Test suite
├── docs/                 # Documentation
├── scripts/              # Utility scripts
└── config/               # Configuration files
```

## Docker

### Development with Docker Compose

```bash
# Start all services (API + PostgreSQL + Redis)
make docker-up

# View logs
make docker-logs

# Stop services
make docker-down
```

### Build Production Image

```bash
docker build -t my-api .
docker run -p 8000:8000 my-api
```

## Configuration

Configuration is managed through environment variables. See `.env.example` for all options.

Key settings:

| Variable | Description | Default |
|----------|-------------|---------|
| `APP_NAME` | Application name | `my-api` |
| `APP_ENV` | Environment | `local` |
| `DEBUG` | Enable debug mode | `false` |
| `DATABASE_HOST` | PostgreSQL host | `localhost` |
| `REDIS_HOST` | Redis host | `localhost` |

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/v1/health` | Health check |
| GET | `/api/v1/health/ready` | Readiness probe |
| GET | `/api/v1/health/live` | Liveness probe |

## Development

### Adding a New Endpoint

1. Create route module in `src/api/routes/`
2. Create schemas in `src/api/schemas/`
3. Create service in `src/services/` (if needed)
4. Include router in `src/api/main.py`
5. Add tests in `tests/`

### Code Style

- **Linting**: Ruff
- **Formatting**: Ruff
- **Type Checking**: Mypy (strict mode)

Pre-commit hooks enforce code quality automatically.

## Documentation

- [CLAUDE.md](CLAUDE.md) - AI assistant guide
- [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) - System architecture
- [docs/DEVELOPMENT.md](docs/DEVELOPMENT.md) - Development guide

## License

MIT License - see LICENSE file for details.
