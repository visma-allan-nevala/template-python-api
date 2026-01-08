# =============================================================================
# Dockerfile for FastAPI Application
# =============================================================================
# Multi-stage build for smaller production images
#
# Build: docker build -t my-api .
# Run:   docker run -p 8000:8000 my-api
# =============================================================================

# -----------------------------------------------------------------------------
# Stage 1: Builder - Install dependencies
# -----------------------------------------------------------------------------
FROM python:3.14-slim AS builder

# Install uv for fast dependency management
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

# Set environment variables
ENV UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy \
    UV_PYTHON_DOWNLOADS=never \
    UV_PROJECT_ENVIRONMENT=/app/.venv

WORKDIR /app

# Copy dependency files first (for better caching)
COPY pyproject.toml uv.lock* ./

# Install dependencies (without dev dependencies)
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-dev --no-install-project

# -----------------------------------------------------------------------------
# Stage 2: Runtime - Final production image
# -----------------------------------------------------------------------------
FROM python:3.14-slim AS runtime

# Create non-root user for security
RUN groupadd --gid 1000 appgroup && \
    useradd --uid 1000 --gid 1000 --shell /bin/bash --create-home appuser

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONFAULTHANDLER=1 \
    PATH="/app/.venv/bin:$PATH" \
    # Application defaults (override via environment)
    APP_ENV=production \
    API_HOST=0.0.0.0 \
    API_PORT=8000

WORKDIR /app

# Copy virtual environment from builder
COPY --from=builder /app/.venv /app/.venv

# Copy application source code
COPY --chown=appuser:appgroup src/ ./src/

# Copy any additional required files
# COPY --chown=appuser:appgroup config/ ./config/
# COPY --chown=appuser:appgroup scripts/run_migrations.sh ./scripts/

# Switch to non-root user
USER appuser

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import httpx; httpx.get('http://localhost:8000/api/v1/health')" || exit 1

# Run the application
# Use exec form to ensure proper signal handling
CMD ["uvicorn", "src.api.main:app", "--host", "0.0.0.0", "--port", "8000"]

# -----------------------------------------------------------------------------
# Development target (optional)
# Build with: docker build --target development -t my-api:dev .
# -----------------------------------------------------------------------------
FROM builder AS development

# Install uv in development image
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

# Install all dependencies including dev
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-install-project

# Copy source code
COPY . .

# Set development environment
ENV APP_ENV=local \
    DEBUG=true \
    PATH="/app/.venv/bin:$PATH"

EXPOSE 8000

# Run with reload for development
CMD ["uvicorn", "src.api.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
