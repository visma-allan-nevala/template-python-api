# API Documentation

This document describes the API endpoints, authentication, and usage.

## Base URL

| Environment | URL |
|-------------|-----|
| Local | `http://localhost:8000` |
| Development | `https://api-dev.example.com` |
| Staging | `https://api-staging.example.com` |
| Production | `https://api.example.com` |

## Authentication

### API Key Authentication

Include the API key in the `X-API-Key` header:

```bash
curl -X GET "https://api.example.com/api/v1/resource" \
  -H "X-API-Key: your-api-key"
```

### JWT Authentication (if enabled)

Include the JWT token in the `Authorization` header:

```bash
curl -X GET "https://api.example.com/api/v1/resource" \
  -H "Authorization: Bearer your-jwt-token"
```

## Endpoints

### Health Check

#### GET /api/v1/health

Basic health check endpoint.

**Response:**
```json
{
  "status": "healthy",
  "service": "my-api",
  "version": "0.1.0"
}
```

#### GET /api/v1/health/ready

Readiness probe for Kubernetes.

**Response:**
```json
{
  "status": "ready",
  "checks": {
    "database": true,
    "redis": true
  }
}
```

#### GET /api/v1/health/live

Liveness probe for Kubernetes.

**Response:**
```json
{
  "status": "alive",
  "service": "my-api",
  "version": "0.1.0"
}
```

## Error Responses

All errors follow a consistent format:

```json
{
  "error": {
    "code": "ERROR_CODE",
    "message": "Human-readable error message",
    "details": {}
  }
}
```

### Error Codes

| Code | HTTP Status | Description |
|------|-------------|-------------|
| `VALIDATION_ERROR` | 400 | Invalid request data |
| `UNAUTHORIZED` | 401 | Authentication required |
| `FORBIDDEN` | 403 | Permission denied |
| `NOT_FOUND` | 404 | Resource not found |
| `CONFLICT` | 409 | Resource conflict |
| `RATE_LIMITED` | 429 | Too many requests |
| `INTERNAL_ERROR` | 500 | Server error |

## Rate Limiting

API requests are rate limited per client.

**Headers:**
- `X-RateLimit-Limit`: Maximum requests per window
- `X-RateLimit-Remaining`: Remaining requests
- `X-RateLimit-Reset`: Unix timestamp when window resets

When rate limited, the API returns:
```json
{
  "error": {
    "code": "RATE_LIMITED",
    "message": "Too many requests"
  }
}
```

## Pagination

List endpoints support pagination:

**Query Parameters:**
- `page`: Page number (default: 1)
- `page_size`: Items per page (default: 20, max: 100)

**Response:**
```json
{
  "items": [...],
  "total": 100,
  "page": 1,
  "page_size": 20,
  "pages": 5
}
```

## OpenAPI Documentation

Interactive API documentation is available at:

- **Swagger UI**: `/docs`
- **ReDoc**: `/redoc`
- **OpenAPI JSON**: `/openapi.json`

> Note: Documentation endpoints are disabled in production by default.
