"""
API Routes package.

This package contains all API endpoint definitions organized by domain.
Each module defines a router with related endpoints.

Modules
-------
health : Health check endpoints
    Provides liveness and readiness probes for Kubernetes deployments.

Adding New Routes
-----------------
1. Create a new module (e.g., `users.py`)
2. Define a router with prefix and tags
3. Add route handlers
4. Include the router in `main.py`

Example
-------
Create `users.py`::

    from fastapi import APIRouter, HTTPException, status
    from src.api.schemas.users import UserCreate, UserResponse

    router = APIRouter(prefix="/users", tags=["users"])

    @router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
    async def create_user(user: UserCreate):
        # Implementation
        pass

    @router.get("/{user_id}", response_model=UserResponse)
    async def get_user(user_id: str):
        # Implementation
        pass

Then in `main.py`::

    from src.api.routes import users
    app.include_router(users.router, prefix="/api/v1")

Route Organization Guidelines
-----------------------------
- Group related endpoints in the same module
- Use meaningful prefixes (e.g., `/users`, `/orders`)
- Add descriptive tags for OpenAPI documentation
- Keep route handlers thin - delegate to services
- Use dependency injection for services and database sessions
"""
