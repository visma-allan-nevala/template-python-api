"""
Authentication Middleware.

Handles API key, JWT, and OAuth authentication for protected endpoints.

Usage
-----
Add to your FastAPI app in `main.py`::

    from src.api.middleware.auth import AuthMiddleware
    app.add_middleware(AuthMiddleware)

Or use as a dependency for specific routes::

    from src.api.middleware.auth import get_current_user

    @router.get("/protected")
    async def protected_route(user: User = Depends(get_current_user)):
        return {"user": user}

Configuration
-------------
Set these environment variables:

- `API_KEYS`: Comma-separated list of valid API keys
- `JWT_ENABLED`: Enable JWT authentication (true/false)
- `JWT_SECRET`: Secret key for JWT validation
- `OAUTH_ENABLED`: Enable OAuth authentication (true/false)
- `OAUTH_ISSUER`: OAuth provider issuer URL

Authentication Flow
-------------------
1. Check for API key in `X-API-Key` header
2. If not found, check for JWT in `Authorization: Bearer <token>` header
3. If not found, check for OAuth token
4. If no valid credentials, return 401 Unauthorized

Public Endpoints
----------------
Some endpoints don't require authentication (e.g., health checks).
Configure these in the middleware or use separate routers.
"""

from typing import Any

from fastapi import Depends, HTTPException, Security, status
from fastapi.security import APIKeyHeader, HTTPAuthorizationCredentials, HTTPBearer

from src.core.config import settings

# Security schemes
api_key_header = APIKeyHeader(name="X-API-Key", auto_error=False)
bearer_scheme = HTTPBearer(auto_error=False)


async def verify_api_key(api_key: str | None = Security(api_key_header)) -> str | None:
    """
    Verify API key from X-API-Key header.

    Parameters
    ----------
    api_key : str | None
        API key from header

    Returns
    -------
    str | None
        Valid API key or None

    Raises
    ------
    HTTPException
        If API key is invalid
    """
    if api_key is None:
        return None

    if api_key not in settings.api_keys:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid API key",
        )

    return api_key


async def verify_bearer_token(
    credentials: HTTPAuthorizationCredentials | None = Security(bearer_scheme),
) -> dict[str, Any] | None:
    """
    Verify JWT or OAuth token from Authorization header.

    Parameters
    ----------
    credentials : HTTPAuthorizationCredentials | None
        Bearer token credentials

    Returns
    -------
    dict | None
        Decoded token payload or None

    Raises
    ------
    HTTPException
        If token is invalid
    """
    if credentials is None:
        return None

    _token = credentials.credentials

    # TODO: Implement JWT verification
    # if settings.jwt_enabled:
    #     try:
    #         payload = jwt.decode(
    #             token,
    #             settings.jwt_secret,
    #             algorithms=[settings.jwt_algorithm],
    #             audience=settings.jwt_audience,
    #             issuer=settings.jwt_issuer,
    #         )
    #         return payload
    #     except jwt.InvalidTokenError as e:
    #         raise HTTPException(
    #             status_code=status.HTTP_401_UNAUTHORIZED,
    #             detail=f"Invalid token: {e}",
    #         )

    # TODO: Implement OAuth verification
    # if settings.oauth_enabled:
    #     # Verify token with OAuth provider
    #     pass

    # For now, reject all bearer tokens
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Bearer token authentication not configured",
    )


async def get_current_user(
    api_key: str | None = Depends(verify_api_key),
    token_payload: dict[str, Any] | None = Depends(verify_bearer_token),
) -> dict[str, Any]:
    """
    Get current authenticated user/client.

    This dependency checks authentication and returns user information.
    Use this for protected endpoints.

    Parameters
    ----------
    api_key : str | None
        Verified API key
    token_payload : dict | None
        Decoded token payload

    Returns
    -------
    dict
        User/client information

    Raises
    ------
    HTTPException
        If not authenticated

    Example
    -------
    ::

        @router.get("/protected")
        async def protected_route(user: dict = Depends(get_current_user)):
            return {"authenticated_as": user}
    """
    if api_key:
        return {"type": "api_key", "key_prefix": api_key[:8] + "..."}

    if token_payload:
        return {"type": "token", "payload": token_payload}

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Authentication required",
        headers={"WWW-Authenticate": "Bearer"},
    )


# Optional: Full middleware implementation
# Uncomment and customize as needed

# from starlette.middleware.base import BaseHTTPMiddleware
# from starlette.requests import Request
# from starlette.responses import Response, JSONResponse
#
# PUBLIC_PATHS = {"/api/v1/health", "/api/v1/health/ready", "/api/v1/health/live"}
#
# class AuthMiddleware(BaseHTTPMiddleware):
#     """Authentication middleware for all requests."""
#
#     async def dispatch(self, request: Request, call_next) -> Response:
#         # Skip auth for public paths
#         if request.url.path in PUBLIC_PATHS:
#             return await call_next(request)
#
#         # Check API key
#         api_key = request.headers.get("X-API-Key")
#         if api_key and api_key in settings.api_keys:
#             return await call_next(request)
#
#         # Check bearer token
#         auth_header = request.headers.get("Authorization")
#         if auth_header and auth_header.startswith("Bearer "):
#             # TODO: Validate token
#             pass
#
#         return JSONResponse(
#             status_code=401,
#             content={"error": {"code": "UNAUTHORIZED", "message": "Authentication required"}},
#         )
