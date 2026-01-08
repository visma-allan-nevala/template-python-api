"""
API layer package.

This package contains the FastAPI application setup, HTTP routes,
request/response schemas, and middleware components.

Modules
-------
main : FastAPI application
    The main FastAPI app instance with lifecycle events, exception handlers,
    and router configuration. This is the ASGI entry point.

Subpackages
-----------
routes : API endpoint definitions
    Each module defines routes for a specific domain (health, users, etc.).
    Routes handle HTTP requests and delegate to services.

schemas : Pydantic models
    Request and response schemas for API validation and serialization.
    These ensure type safety at API boundaries.

middleware : Request/response middleware
    Components that process requests before routes and responses after.
    Includes authentication, logging, rate limiting, etc.

Usage
-----
The main app is exposed for ASGI servers:

    from src.api.main import app

    # Run with uvicorn
    uvicorn src.api.main:app --reload

Adding New Routes
-----------------
1. Create a new module in `routes/` (e.g., `routes/users.py`)
2. Define a router: `router = APIRouter(prefix="/users", tags=["users"])`
3. Add route handlers with appropriate HTTP methods
4. Include the router in `main.py`

Example route module::

    from fastapi import APIRouter, Depends
    from src.api.schemas.users import UserResponse
    from src.services.user_service import UserService

    router = APIRouter(prefix="/users", tags=["users"])

    @router.get("/{user_id}", response_model=UserResponse)
    async def get_user(user_id: str, service: UserService = Depends()):
        return await service.get_user(user_id)
"""
