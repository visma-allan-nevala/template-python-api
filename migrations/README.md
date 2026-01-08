# Database Migrations

This folder contains database migration files.

## Recommended: Alembic

For production applications, we recommend using [Alembic](https://alembic.sqlalchemy.org/) for database migrations.

### Setup Alembic

```bash
# Install Alembic (included in db dependencies)
uv sync --extra db

# Initialize Alembic
uv run alembic init migrations

# Configure alembic.ini with your database URL
# Edit migrations/env.py to import your models
```

### Create a Migration

```bash
# Auto-generate migration from model changes
uv run alembic revision --autogenerate -m "Add users table"

# Create empty migration
uv run alembic revision -m "Add custom migration"
```

### Run Migrations

```bash
# Apply all pending migrations
uv run alembic upgrade head

# Rollback one migration
uv run alembic downgrade -1

# Show current revision
uv run alembic current

# Show migration history
uv run alembic history
```

## Alternative: Raw SQL

For simpler projects, you can use raw SQL files:

```
migrations/
├── 001_create_users.sql
├── 002_add_email_index.sql
└── 003_create_orders.sql
```

Run with `scripts/run_migrations.sh` (modify to execute SQL files).

## Migration Best Practices

1. **Always test migrations** on a copy of production data
2. **Make migrations reversible** when possible
3. **Use transactions** for atomicity
4. **Avoid data loss** - add columns before removing old ones
5. **Keep migrations small** and focused
6. **Version control** all migration files
7. **Document breaking changes** in migration comments

## Kubernetes Deployment

Migrations run automatically via init container. See `docs/DEVELOPMENT.md` for details.
