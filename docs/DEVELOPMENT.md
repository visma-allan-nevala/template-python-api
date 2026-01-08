# Development Guide

This guide covers setting up your development environment and common development tasks.

## Prerequisites

- **Python 3.12+** - Required Python version
- **uv** - Fast Python package manager ([install guide](https://docs.astral.sh/uv/))
- **Docker** - For running PostgreSQL and Redis locally
- **Git** - Version control

## Initial Setup

### 1. Clone and Setup

```bash
# Clone the repository
git clone https://github.com/your-org/my-api.git
cd my-api

# Run automated setup
./setup.sh

# This will:
# 1. Check Python version
# 2. Install uv if needed
# 3. Install dependencies
# 4. Install pre-commit hooks
# 5. Create .env from .env.example
```

### 2. Configure Environment

Edit `.env` with your settings:

```bash
# Required for local development
APP_NAME=my-api
APP_ENV=local
DEBUG=true

# Database (if using Docker Compose, these work out of the box)
DATABASE_HOST=localhost
DATABASE_PORT=5432
DATABASE_USER=app_user
DATABASE_PASSWORD=app_password
DATABASE_NAME=app_db
```

### 3. Start Services

```bash
# Start PostgreSQL and Redis
make docker-up

# Verify services are running
docker-compose ps
```

### 4. Run the Application

```bash
# Start development server with hot reload
make dev

# Or manually:
uv run uvicorn src.api.main:app --reload --host 0.0.0.0 --port 8000
```

Visit http://localhost:8000/docs to see the API documentation.

## Common Commands

### Development

| Command | Description |
|---------|-------------|
| `make dev` | Start dev server with hot reload |
| `make test` | Run all tests |
| `make test-v` | Run tests with verbose output |
| `make test-cov` | Run tests with coverage report |
| `make check` | Run linting and type checking |
| `make lint-fix` | Auto-fix lint issues |

### Docker

| Command | Description |
|---------|-------------|
| `make docker-up` | Start all services |
| `make docker-down` | Stop all services |
| `make docker-logs` | View container logs |
| `make docker-clean` | Stop services and remove volumes |

### Dependencies

| Command | Description |
|---------|-------------|
| `uv sync` | Install dependencies |
| `uv sync --extra dev` | Include dev dependencies |
| `uv add <package>` | Add a new dependency |
| `uv lock` | Update lock file |

## Adding New Features

### 1. Add a New API Endpoint

**Step 1: Create the route module**

```python
# src/api/routes/items.py
from fastapi import APIRouter, Depends, HTTPException, status

from src.api.schemas.items import ItemCreate, ItemResponse
from src.services.item_service import ItemService

router = APIRouter(prefix="/items", tags=["items"])

@router.post("/", response_model=ItemResponse, status_code=status.HTTP_201_CREATED)
async def create_item(
    data: ItemCreate,
    service: ItemService = Depends(),
) -> ItemResponse:
    """Create a new item."""
    return await service.create_item(data)

@router.get("/{item_id}", response_model=ItemResponse)
async def get_item(
    item_id: str,
    service: ItemService = Depends(),
) -> ItemResponse:
    """Get an item by ID."""
    item = await service.get_item(item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return item
```

**Step 2: Create the schemas**

```python
# src/api/schemas/items.py
from pydantic import BaseModel, Field

class ItemBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    description: str | None = None

class ItemCreate(ItemBase):
    pass

class ItemResponse(ItemBase):
    id: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
```

**Step 3: Include the router in main.py**

```python
# src/api/main.py
from src.api.routes import items

app.include_router(items.router, prefix="/api/v1")
```

**Step 4: Add tests**

```python
# tests/unit/test_items.py
def test_create_item(client):
    response = client.post("/api/v1/items", json={"name": "Test"})
    assert response.status_code == 201
```

### 2. Add a New Service

```python
# src/services/item_service.py
from src.core.exceptions import NotFoundError

class ItemService:
    def __init__(self, repository: ItemRepository):
        self.repository = repository

    async def get_item(self, item_id: str) -> Item:
        item = await self.repository.get_by_id(item_id)
        if not item:
            raise NotFoundError("Item", item_id)
        return item

    async def create_item(self, data: ItemCreate) -> Item:
        return await self.repository.create(data)
```

### 3. Add a New Database Model

```python
# src/models/item.py
from sqlalchemy import String, DateTime
from sqlalchemy.orm import Mapped, mapped_column
from src.models.base import Base

class Item(Base):
    __tablename__ = "items"

    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
```

## Testing

### Run Tests

```bash
# All tests
make test

# Specific test file
uv run pytest tests/unit/test_health.py -v

# Specific test function
uv run pytest tests/unit/test_health.py::test_health_check -v

# With coverage
make test-cov
```

### Test Organization

```
tests/
├── conftest.py          # Shared fixtures
├── unit/                # Fast, isolated tests
│   └── test_health.py
├── integration/         # Tests with real dependencies
└── smoke/               # Tests for deployed environments
```

### Writing Tests

```python
# tests/unit/test_item_service.py
import pytest
from unittest.mock import AsyncMock

@pytest.fixture
def mock_repository():
    return AsyncMock()

@pytest.fixture
def service(mock_repository):
    return ItemService(mock_repository)

async def test_get_item_not_found(service, mock_repository):
    mock_repository.get_by_id.return_value = None

    with pytest.raises(NotFoundError):
        await service.get_item("nonexistent")
```

## Debugging

### Enable Debug Mode

Set in `.env`:
```
DEBUG=true
LOG_LEVEL=DEBUG
```

### View Logs

```bash
# Application logs
make dev  # Logs appear in terminal

# Docker service logs
make docker-logs
```

### Debug with VS Code

Add to `.vscode/launch.json`:

```json
{
  "version": "0.2.0",
  "configurations": [
    {
      "name": "FastAPI",
      "type": "python",
      "request": "launch",
      "module": "uvicorn",
      "args": ["src.api.main:app", "--reload"],
      "jinja": true
    }
  ]
}
```

## Code Quality

### Pre-commit Hooks

Hooks run automatically on commit:
- **Ruff**: Linting and formatting
- **Mypy**: Type checking
- **Trailing whitespace**: Cleanup

Run manually:
```bash
uv run pre-commit run --all-files
```

### Type Checking

```bash
uv run mypy src/
```

### Linting

```bash
# Check only
uv run ruff check src/ tests/

# Auto-fix
uv run ruff check src/ tests/ --fix
```

## Troubleshooting

### "Module not found" errors

```bash
# Reinstall dependencies
uv sync --extra dev
```

### Docker services not starting

```bash
# Check for port conflicts
docker-compose ps
docker-compose logs

# Reset completely
make docker-clean
make docker-up
```

### Pre-commit hooks failing

```bash
# Update hooks
uv run pre-commit autoupdate

# Reinstall hooks
uv run pre-commit install --force
```

### Database connection issues

1. Check Docker is running: `docker ps`
2. Verify `.env` settings match `docker-compose.yml`
3. Check PostgreSQL logs: `docker-compose logs postgres`
