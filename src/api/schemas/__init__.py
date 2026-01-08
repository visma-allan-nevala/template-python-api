"""
API Schemas package.

This package contains Pydantic models for request validation and response
serialization. Schemas define the contract between the API and its clients.

Purpose
-------
- Request validation: Ensure incoming data meets requirements
- Response serialization: Control what data is returned to clients
- Documentation: Generate OpenAPI schema automatically
- Type safety: Enable IDE autocompletion and type checking

Modules
-------
health : Health check schemas
    Response models for health check endpoints.

Schema Guidelines
-----------------
1. Use descriptive field names and add Field() descriptions
2. Use appropriate types (str, int, datetime, etc.)
3. Add validation constraints (min_length, ge, le, regex, etc.)
4. Separate request and response models when they differ
5. Use inheritance for shared fields

Example
-------
Create `users.py`::

    from datetime import datetime
    from pydantic import BaseModel, EmailStr, Field

    class UserBase(BaseModel):
        '''Shared user fields.'''
        email: EmailStr = Field(..., description="User's email address")
        name: str = Field(..., min_length=1, max_length=100)

    class UserCreate(UserBase):
        '''Request model for creating a user.'''
        password: str = Field(..., min_length=8, description="User password")

    class UserResponse(UserBase):
        '''Response model for user data.'''
        id: str = Field(..., description="Unique user identifier")
        created_at: datetime = Field(..., description="Account creation timestamp")

        model_config = ConfigDict(from_attributes=True)

Naming Conventions
------------------
- `*Create`: Request body for POST endpoints
- `*Update`: Request body for PUT/PATCH endpoints
- `*Response`: Response model for endpoints
- `*Filter`: Query parameters for filtering
- `*Base`: Shared fields (not used directly in APIs)
"""
