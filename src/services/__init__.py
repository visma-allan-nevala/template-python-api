"""
Services package (Business Logic Layer).

This package contains service classes that implement business logic.
Services are the core of the application, orchestrating data access,
validation, and domain operations.

Architecture
------------
Services sit between the API layer and the storage layer:

    API Routes → Services → Storage/Repositories

Services should:
- Implement business rules and validation
- Coordinate multiple repository calls
- Handle transactions
- Return domain objects or DTOs

Services should NOT:
- Handle HTTP concerns (status codes, headers)
- Directly execute SQL queries
- Contain presentation logic

Usage
-----
Create service classes for each domain::

    from src.services.user_service import UserService

    # In a route handler
    @router.post("/users")
    async def create_user(
        data: UserCreate,
        service: UserService = Depends(get_user_service),
    ):
        return await service.create_user(data)

Example Service
---------------
Create `user_service.py`::

    from src.storage.repositories.user_repository import UserRepository
    from src.core.exceptions import NotFoundError, ConflictError

    class UserService:
        def __init__(self, repository: UserRepository):
            self.repository = repository

        async def get_user(self, user_id: str) -> User:
            user = await self.repository.get_by_id(user_id)
            if not user:
                raise NotFoundError("User", user_id)
            return user

        async def create_user(self, data: UserCreate) -> User:
            existing = await self.repository.get_by_email(data.email)
            if existing:
                raise ConflictError(f"User with email {data.email} already exists")
            return await self.repository.create(data)

Dependency Injection
--------------------
Use FastAPI's Depends() for service injection::

    def get_user_service(
        db: AsyncSession = Depends(get_db),
    ) -> UserService:
        repository = UserRepository(db)
        return UserService(repository)

Testing
-------
Services are easily testable with mocked repositories::

    @pytest.fixture
    def mock_repository():
        return AsyncMock(spec=UserRepository)

    @pytest.fixture
    def service(mock_repository):
        return UserService(mock_repository)

    async def test_get_user_not_found(service, mock_repository):
        mock_repository.get_by_id.return_value = None
        with pytest.raises(NotFoundError):
            await service.get_user("nonexistent")
"""
