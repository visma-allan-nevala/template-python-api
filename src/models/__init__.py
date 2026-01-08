"""
Database Models package.

This package contains SQLAlchemy ORM models that define the database schema.
Each model represents a database table and its relationships.

Usage
-----
Import models for use in queries::

    from src.models.user import User

    # In an async session
    result = await session.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()

Model Guidelines
----------------
1. One model per file, named after the entity (e.g., `user.py`)
2. Use a shared `Base` for all models
3. Define relationships explicitly
4. Add indexes for frequently queried columns
5. Use appropriate column types

Example Model
-------------
Create `user.py`::

    from datetime import datetime
    from sqlalchemy import String, DateTime, Boolean
    from sqlalchemy.orm import Mapped, mapped_column
    from src.models.base import Base

    class User(Base):
        '''User account model.'''

        __tablename__ = "users"

        id: Mapped[str] = mapped_column(String(36), primary_key=True)
        email: Mapped[str] = mapped_column(String(255), unique=True, index=True)
        name: Mapped[str] = mapped_column(String(100))
        is_active: Mapped[bool] = mapped_column(Boolean, default=True)
        created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
        updated_at: Mapped[datetime | None] = mapped_column(DateTime, onupdate=datetime.utcnow)

Base Class
----------
Define in `base.py` (not included by default)::

    from sqlalchemy.orm import DeclarativeBase

    class Base(DeclarativeBase):
        '''Base class for all models.'''
        pass

Migrations
----------
Use Alembic for database migrations:

1. Create migration: `uv run alembic revision --autogenerate -m "description"`
2. Apply migration: `uv run alembic upgrade head`
3. Rollback: `uv run alembic downgrade -1`
"""
