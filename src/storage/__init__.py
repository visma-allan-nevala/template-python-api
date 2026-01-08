"""
Storage package (Data Persistence Layer).

This package contains database connections, cache clients, and repository
classes for data access. It abstracts away the details of data storage
from the rest of the application.

Modules
-------
database : Database connection management
    PostgreSQL connection pool and session factory.

redis_client : Redis cache client
    Redis connection and common cache operations.

Subpackages
-----------
repositories : Data access repositories (create as needed)
    Repository classes that encapsulate database queries.

Architecture
------------
The storage layer follows the Repository pattern:

    Services → Repositories → Database/Cache

Repositories provide a clean interface for data operations:
- Abstract away SQL/ORM details
- Enable easy testing with mocks
- Centralize query logic

Usage
-----
Database sessions::

    from src.storage.database import get_db

    @router.get("/items")
    async def get_items(db: AsyncSession = Depends(get_db)):
        result = await db.execute(select(Item))
        return result.scalars().all()

Redis cache::

    from src.storage.redis_client import get_redis

    @router.get("/cached-data")
    async def get_cached(redis = Depends(get_redis)):
        cached = await redis.get("key")
        if cached:
            return json.loads(cached)
        # ... fetch and cache

Repository Pattern
------------------
Create `repositories/user_repository.py`::

    from sqlalchemy import select
    from sqlalchemy.ext.asyncio import AsyncSession
    from src.models.user import User

    class UserRepository:
        def __init__(self, session: AsyncSession):
            self.session = session

        async def get_by_id(self, user_id: str) -> User | None:
            result = await self.session.execute(
                select(User).where(User.id == user_id)
            )
            return result.scalar_one_or_none()

        async def create(self, user: User) -> User:
            self.session.add(user)
            await self.session.commit()
            await self.session.refresh(user)
            return user

Connection Lifecycle
--------------------
- Connections are created lazily on first use
- Connection pools manage connection reuse
- Connections are closed on application shutdown
- Use async context managers for transactions
"""
