# Security Documentation

This document describes security measures, authentication, and best practices for this API.

## Authentication

### Supported Methods

1. **API Key** - Simple key-based authentication
2. **JWT** - JSON Web Token authentication (optional)
3. **OAuth 2.0** - OAuth token validation (optional)

### API Key Authentication

API keys are validated against the `API_KEYS` environment variable.

**Usage:**
```bash
curl -H "X-API-Key: your-api-key" https://api.example.com/api/v1/resource
```

**Key Management:**
- Generate keys: `python scripts/generate_api_keys.py`
- Rotate keys: `python scripts/rotate_api_keys.py`
- Store keys securely (environment variables or secret manager)

### JWT Authentication

When enabled (`JWT_ENABLED=true`), JWT tokens are validated:

- Signature verification with `JWT_SECRET`
- Issuer validation (`JWT_ISSUER`)
- Audience validation (`JWT_AUDIENCE`)
- Expiration checking

## Authorization

Authorization is handled at the route level using FastAPI dependencies.

```python
@router.get("/admin")
async def admin_route(user: dict = Depends(require_admin)):
    return {"admin": True}
```

## Input Validation

All input is validated using Pydantic schemas:

- Type checking
- Length limits
- Pattern validation
- Custom validators

## Rate Limiting

Rate limiting prevents abuse:

- Default: 100 requests per minute per client
- Configurable via environment variables
- Redis-backed for multi-instance deployments

## Security Headers

Recommended security headers (configure in reverse proxy):

```
X-Content-Type-Options: nosniff
X-Frame-Options: DENY
X-XSS-Protection: 1; mode=block
Strict-Transport-Security: max-age=31536000; includeSubDomains
Content-Security-Policy: default-src 'self'
```

## Secrets Management

- **Never commit secrets** to version control
- Use environment variables or secret managers
- Rotate secrets regularly
- Use `.env.example` for documentation only

## Logging

Security events are logged:

- Authentication attempts
- Authorization failures
- Rate limit violations
- Input validation errors

**Important:** Never log sensitive data (passwords, tokens, PII).

## Vulnerability Reporting

Report security vulnerabilities to security@example.com.

## Security Checklist

- [ ] API keys not committed to repository
- [ ] HTTPS enforced in production
- [ ] Rate limiting enabled
- [ ] Input validation on all endpoints
- [ ] Secrets in environment variables
- [ ] Logging excludes sensitive data
- [ ] Dependencies regularly updated
- [ ] Security headers configured
