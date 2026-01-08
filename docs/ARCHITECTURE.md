# Architecture Documentation

This document describes the system architecture, design decisions, and patterns used in this API.

## Overview

This is a FastAPI-based REST API following a layered architecture pattern. The application is designed for:

- **Scalability**: Async I/O, connection pooling, stateless design
- **Maintainability**: Clear separation of concerns, dependency injection
- **Testability**: Layers can be tested independently with mocks
- **Security**: Authentication middleware, input validation, secure defaults

## System Architecture

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                              Client Applications                             │
│                    (Web, Mobile, Internal Services)                          │
└─────────────────────────────────────────────────────────────────────────────┘
                                      │
                                      │ HTTPS
                                      ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                           Load Balancer / Ingress                            │
│                        (Kubernetes Ingress, ALB, etc.)                       │
└─────────────────────────────────────────────────────────────────────────────┘
                                      │
                                      ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                              API Application                                 │
│  ┌───────────────────────────────────────────────────────────────────────┐  │
│  │                         Middleware Layer                               │  │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  │  │
│  │  │    Auth     │  │   Logging   │  │ Rate Limit  │  │    CORS     │  │  │
│  │  └─────────────┘  └─────────────┘  └─────────────┘  └─────────────┘  │  │
│  └───────────────────────────────────────────────────────────────────────┘  │
│                                      │                                       │
│                                      ▼                                       │
│  ┌───────────────────────────────────────────────────────────────────────┐  │
│  │                           API Layer                                    │  │
│  │  Routes (endpoints) → Schemas (validation) → Dependencies             │  │
│  └───────────────────────────────────────────────────────────────────────┘  │
│                                      │                                       │
│                                      ▼                                       │
│  ┌───────────────────────────────────────────────────────────────────────┐  │
│  │                         Service Layer                                  │  │
│  │  Business logic, orchestration, domain rules                          │  │
│  └───────────────────────────────────────────────────────────────────────┘  │
│                                      │                                       │
│                                      ▼                                       │
│  ┌───────────────────────────────────────────────────────────────────────┐  │
│  │                         Storage Layer                                  │  │
│  │  Database clients, cache clients, repositories                        │  │
│  └───────────────────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────────────────┘
                    │                                    │
                    ▼                                    ▼
          ┌─────────────────┐                  ┌─────────────────┐
          │   PostgreSQL    │                  │     Redis       │
          │   (Primary DB)  │                  │    (Cache)      │
          └─────────────────┘                  └─────────────────┘
```

## Layer Responsibilities

### 1. Middleware Layer (`src/api/middleware/`)

Processes all requests/responses before they reach route handlers.

| Component | Responsibility |
|-----------|---------------|
| `auth.py` | Authentication (API key, JWT, OAuth) |
| `logging.py` | Request/response logging, request IDs |
| `rate_limit.py` | Rate limiting per client |

**Key Principle**: Middleware should be stateless and fast.

### 2. API Layer (`src/api/`)

Handles HTTP concerns: routing, request validation, response serialization.

| Component | Responsibility |
|-----------|---------------|
| `routes/` | HTTP endpoint definitions |
| `schemas/` | Pydantic models for validation |
| `main.py` | App initialization, router configuration |

**Key Principle**: Routes should be thin - delegate to services.

### 3. Service Layer (`src/services/`)

Contains business logic and orchestrates data access.

**Responsibilities**:
- Business rule validation
- Orchestrating multiple repository calls
- Transaction management
- Domain logic

**Key Principle**: Services should be testable with mocked repositories.

### 4. Storage Layer (`src/storage/`)

Handles all data persistence and caching.

| Component | Responsibility |
|-----------|---------------|
| `database.py` | PostgreSQL connection management |
| `redis_client.py` | Redis connection management |
| `repositories/` | Data access patterns (create as needed) |

**Key Principle**: Never expose database details to upper layers.

## Data Flow

### Request Flow

```
1. Request arrives at load balancer
2. Routed to API instance
3. Middleware pipeline executes:
   - Auth validates credentials
   - Logging records request
   - Rate limit checks quotas
4. Route handler receives validated request
5. Service layer executes business logic
6. Storage layer retrieves/persists data
7. Response flows back through middleware
8. JSON response sent to client
```

### Example: Create Resource

```
POST /api/v1/resources
     │
     ▼
┌─────────────────┐
│  Auth Middleware │ → Validate API key/JWT
└────────┬────────┘
         ▼
┌─────────────────┐
│   Route Handler  │ → Validate request body (Pydantic)
└────────┬────────┘
         ▼
┌─────────────────┐
│ ResourceService  │ → Check business rules
└────────┬────────┘   → Create resource
         ▼
┌─────────────────┐
│ ResourceRepo     │ → INSERT into database
└────────┬────────┘
         ▼
    201 Created
```

## Design Patterns

### Dependency Injection

FastAPI's `Depends()` system for injecting services and database sessions:

```python
@router.get("/items/{item_id}")
async def get_item(
    item_id: str,
    db: AsyncSession = Depends(get_db),
    service: ItemService = Depends(get_item_service),
):
    return await service.get_item(item_id)
```

### Repository Pattern

Encapsulates data access logic:

```python
class ItemRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_id(self, item_id: str) -> Item | None:
        result = await self.session.execute(
            select(Item).where(Item.id == item_id)
        )
        return result.scalar_one_or_none()
```

### Factory Pattern

For creating complex objects:

```python
def create_application() -> FastAPI:
    app = FastAPI(...)
    # Configure middleware, routes, etc.
    return app
```

## Configuration

Configuration follows the 12-factor app methodology:

1. **Environment variables** are the source of truth
2. **Pydantic Settings** validates and provides defaults
3. **No secrets in code** - use environment or secret managers

See `src/core/config.py` for implementation.

## Error Handling

Consistent error responses:

```json
{
  "error": {
    "code": "NOT_FOUND",
    "message": "Resource with ID '123' not found",
    "details": {"entity": "Resource", "id": "123"}
  }
}
```

See `src/core/exceptions.py` for custom exception classes.

## Security

### Authentication

Multiple authentication methods supported:

1. **API Key**: `X-API-Key` header
2. **JWT**: `Authorization: Bearer <token>` header
3. **OAuth**: Token validation with OAuth provider

### Input Validation

- All inputs validated with Pydantic
- SQL injection prevented by ORM
- Rate limiting prevents abuse

## Deployment

### Local Development

```bash
make dev  # Hot reload enabled
```

### Docker

```bash
docker-compose up  # API + PostgreSQL + Redis
```

### Kubernetes

- Use the provided Dockerfile
- Configure via environment variables
- Health probes at `/api/v1/health/ready` and `/api/v1/health/live`
