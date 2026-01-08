"""
Database Connection Management.

Provides async PostgreSQL connection pool and session management using SQLAlchemy.

Usage
-----
In route handlers with dependency injection::

    from src.storage.database import get_db

    @router.get("/items")
    async def get_items(db: AsyncSession = Depends(get_db)):
        result = await db.execute(select(Item))
        return result.scalars().all()

In services or background tasks::

    from src.storage.database import async_session_factory

    async with async_session_factory() as session:
        result = await session.execute(select(Item))
        items = result.scalars().all()

Transactions::

    async with async_session_factory() as session:
        async with session.begin():
            session.add(item1)
            session.add(item2)
            # Auto-commits on exit, rolls back on exception

Configuration
-------------
Database settings are loaded from environment variables:
- DATABASE_HOST
- DATABASE_PORT
- DATABASE_USER
- DATABASE_PASSWORD
- DATABASE_NAME
- DATABASE_SSL
"""

from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager
from typing import Any

from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from src.core.config import settings

# Engine configuration
_engine: AsyncEngine | None = None

# Session factory
_async_session_factory: async_sessionmaker[AsyncSession] | None = None


def get_engine() -> AsyncEngine:
    """
    Get or create the database engine.

    Returns
    -------
    AsyncEngine
        SQLAlchemy async engine instance
    """
    global _engine

    if _engine is None:
        _engine = create_async_engine(
            settings.database.url,
            echo=settings.debug,  # Log SQL in debug mode
            pool_size=5,
            max_overflow=10,
            pool_pre_ping=True,  # Verify connections before use
            pool_recycle=3600,  # Recycle connections after 1 hour
        )

    return _engine


def get_session_factory() -> async_sessionmaker[AsyncSession]:
    """
    Get or create the session factory.

    Returns
    -------
    async_sessionmaker
        SQLAlchemy async session factory
    """
    global _async_session_factory

    if _async_session_factory is None:
        _async_session_factory = async_sessionmaker(
            bind=get_engine(),
            class_=AsyncSession,
            expire_on_commit=False,
            autoflush=False,
        )

    return _async_session_factory


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """
    Dependency for getting database sessions in route handlers.

    Yields
    ------
    AsyncSession
        Database session that auto-closes after request

    Example
    -------
    ::

        @router.get("/items")
        async def get_items(db: AsyncSession = Depends(get_db)):
            result = await db.execute(select(Item))
            return result.scalars().all()
    """
    factory = get_session_factory()
    async with factory() as session:
        try:
            yield session
        finally:
            await session.close()


@asynccontextmanager
async def async_session_context() -> AsyncGenerator[AsyncSession, None]:
    """
    Context manager for database sessions outside of request handlers.

    Use this in background tasks or scripts.

    Example
    -------
    ::

        async with async_session_context() as session:
            result = await session.execute(select(Item))
            items = result.scalars().all()
    """
    factory = get_session_factory()
    async with factory() as session:
        try:
            yield session
        finally:
            await session.close()


async def init_database() -> None:
    """
    Initialize database connection pool.

    Call this during application startup to eagerly create connections.
    """
    engine = get_engine()
    # Verify connectivity
    async with engine.begin() as conn:
        await conn.execute("SELECT 1")  # type: ignore[arg-type]


async def close_database() -> None:
    """
    Close database connection pool.

    Call this during application shutdown to cleanly close connections.
    """
    global _engine, _async_session_factory

    if _engine is not None:
        await _engine.dispose()
        _engine = None
        _async_session_factory = None


async def execute_raw_sql(sql: str, params: dict[str, Any] | None = None) -> Any:
    """
    Execute raw SQL query.

    Use sparingly - prefer ORM queries for type safety.

    Parameters
    ----------
    sql : str
        SQL query string
    params : dict | None
        Query parameters

    Returns
    -------
    Any
        Query result
    """
    engine = get_engine()
    async with engine.begin() as conn:
        result = await conn.execute(sql, params or {})  # type: ignore[arg-type]
        return result
