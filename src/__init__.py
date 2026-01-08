"""
Source package for the API application.

This is the root package containing all application code organized into
logical subpackages following a layered architecture pattern.

Subpackages
-----------
api : FastAPI application layer
    Contains the FastAPI app, routes, request/response schemas, and middleware.
    This is the entry point for HTTP requests.

adapters : External service adapters
    Contains adapter classes that abstract external APIs and services.
    Adapters provide a consistent interface for external integrations.

core : Core configuration and utilities
    Contains configuration management, constants, custom exceptions, and
    other foundational components used across the application.

models : Database models
    Contains SQLAlchemy ORM models defining the database schema.
    Each model represents a database table.

services : Business logic layer
    Contains service classes that implement business logic.
    Services are called by API routes and may use multiple adapters/repositories.

storage : Data persistence layer
    Contains database connections, cache clients, and repository classes
    for data access patterns.

utils : Utility functions
    Contains helper functions and utilities used across the application.

Architecture
------------
The application follows a layered architecture:

    HTTP Request
         │
         ▼
    ┌─────────┐
    │   API   │  Routes, Schemas, Middleware
    └────┬────┘
         │
         ▼
    ┌─────────┐
    │ Services│  Business Logic
    └────┬────┘
         │
    ┌────┴────┐
    │         │
    ▼         ▼
┌─────────┐ ┌─────────┐
│ Storage │ │Adapters │  External APIs
└─────────┘ └─────────┘

Example
-------
To run the application:

    uvicorn src.api.main:app --reload
"""
