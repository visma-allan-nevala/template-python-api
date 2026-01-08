"""
API Middleware package.

This package contains middleware components that process requests and responses.
Middleware runs before route handlers (request processing) and after (response processing).

Modules
-------
auth : Authentication middleware
    Validates API keys, JWT tokens, or OAuth tokens on protected routes.

logging : Request/response logging
    Logs request details and response times for monitoring and debugging.

rate_limit : Rate limiting
    Prevents abuse by limiting requests per client/IP.

How Middleware Works
--------------------
Middleware wraps the request/response cycle:

    Request → [Middleware A] → [Middleware B] → [Route Handler]
                                                       │
    Response ← [Middleware A] ← [Middleware B] ←──────┘

Each middleware can:
- Modify the request before passing to the next middleware
- Short-circuit by returning a response directly
- Modify the response before returning to the client
- Perform cleanup after the response is sent

Adding Middleware
-----------------
There are two patterns for middleware in FastAPI:

1. **ASGI Middleware** (recommended for most cases)::

    from starlette.middleware.base import BaseHTTPMiddleware
    from starlette.requests import Request
    from starlette.responses import Response

    class MyMiddleware(BaseHTTPMiddleware):
        async def dispatch(self, request: Request, call_next) -> Response:
            # Before request
            response = await call_next(request)
            # After response
            return response

    # In main.py
    app.add_middleware(MyMiddleware)

2. **Pure ASGI Middleware** (for maximum performance)::

    class MyMiddleware:
        def __init__(self, app):
            self.app = app

        async def __call__(self, scope, receive, send):
            if scope["type"] != "http":
                await self.app(scope, receive, send)
                return

            # Custom logic here
            await self.app(scope, receive, send)

Middleware Order
----------------
Middleware is executed in reverse order of addition:

    app.add_middleware(A)  # Runs second
    app.add_middleware(B)  # Runs first

So the last added middleware is the outermost wrapper.
"""
