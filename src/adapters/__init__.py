"""
Adapters package for external service integrations.

This package contains adapter classes that abstract external APIs and services.
Adapters provide a consistent interface for the rest of the application to
interact with external systems, enabling easy swapping of implementations
and better testability.

Architecture
------------
Adapters sit between services and external systems:

    Services → Adapters → External APIs/Services

Benefits of the Adapter Pattern
-------------------------------
1. **Abstraction**: Hide external API details from business logic
2. **Testability**: Easy to mock adapters in tests
3. **Flexibility**: Swap implementations without changing services
4. **Consistency**: Unified interface across different external systems

Structure
---------
Each external service should have its own subpackage:

    adapters/
    ├── __init__.py
    ├── base.py              # Base adapter class/interface
    ├── external_api/        # Example: External API adapter
    │   ├── __init__.py
    │   ├── adapter.py       # Main adapter implementation
    │   ├── client.py        # HTTP client
    │   ├── models.py        # Response models
    │   └── exceptions.py    # Custom exceptions
    └── payment_gateway/     # Example: Payment gateway adapter
        ├── __init__.py
        └── adapter.py

Example Base Adapter
--------------------
Create `base.py`::

    from abc import ABC, abstractmethod
    from typing import Generic, TypeVar

    T = TypeVar("T")

    class BaseAdapter(ABC, Generic[T]):
        '''Base class for all adapters.'''

        @abstractmethod
        async def get(self, id: str) -> T | None:
            '''Get a resource by ID.'''
            pass

        @abstractmethod
        async def list(self, **filters) -> list[T]:
            '''List resources with optional filters.'''
            pass

Example Implementation
----------------------
Create `external_api/adapter.py`::

    from src.adapters.base import BaseAdapter
    from src.adapters.external_api.client import ExternalAPIClient
    from src.adapters.external_api.models import Resource

    class ExternalAPIAdapter(BaseAdapter[Resource]):
        '''Adapter for External API service.'''

        def __init__(self, client: ExternalAPIClient):
            self.client = client

        async def get(self, id: str) -> Resource | None:
            response = await self.client.get_resource(id)
            if response is None:
                return None
            return Resource.from_api_response(response)

        async def list(self, **filters) -> list[Resource]:
            response = await self.client.list_resources(**filters)
            return [Resource.from_api_response(r) for r in response]

Usage in Services
-----------------
Inject adapters into services::

    class MyService:
        def __init__(self, adapter: ExternalAPIAdapter):
            self.adapter = adapter

        async def get_resource(self, id: str) -> Resource:
            resource = await self.adapter.get(id)
            if not resource:
                raise NotFoundError("Resource", id)
            return resource

Testing
-------
Mock adapters in tests::

    @pytest.fixture
    def mock_adapter():
        return AsyncMock(spec=ExternalAPIAdapter)

    async def test_get_resource(mock_adapter):
        mock_adapter.get.return_value = Resource(id="1", name="Test")
        service = MyService(mock_adapter)
        result = await service.get_resource("1")
        assert result.name == "Test"
"""
