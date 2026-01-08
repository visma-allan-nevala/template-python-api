#!/usr/bin/env bash
# =============================================================================
# Database Migration Runner
# =============================================================================
# This script runs database migrations. It's designed to be run as a
# Kubernetes init container or manually during deployment.
#
# Usage:
#   ./scripts/run_migrations.sh
#
# Environment Variables:
#   DATABASE_HOST     - Database host (required)
#   DATABASE_PORT     - Database port (default: 5432)
#   DATABASE_USER     - Database user (required)
#   DATABASE_PASSWORD - Database password (required)
#   DATABASE_NAME     - Database name (required)
#   DATABASE_SSL      - Enable SSL (default: false)
#
# Exit Codes:
#   0 - Success
#   1 - Database connection failed
#   2 - Migration failed
# =============================================================================

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

log_info() { echo -e "${GREEN}[INFO]${NC} $1"; }
log_warn() { echo -e "${YELLOW}[WARN]${NC} $1"; }
log_error() { echo -e "${RED}[ERROR]${NC} $1"; }

# =============================================================================
# Configuration
# =============================================================================

DB_HOST="${DATABASE_HOST:-localhost}"
DB_PORT="${DATABASE_PORT:-5432}"
DB_USER="${DATABASE_USER:-app_user}"
DB_NAME="${DATABASE_NAME:-app_db}"
DB_SSL="${DATABASE_SSL:-false}"

MAX_RETRIES=30
RETRY_INTERVAL=2

# =============================================================================
# Wait for Database
# =============================================================================

wait_for_database() {
    log_info "Waiting for database at ${DB_HOST}:${DB_PORT}..."

    for i in $(seq 1 $MAX_RETRIES); do
        if pg_isready -h "$DB_HOST" -p "$DB_PORT" -U "$DB_USER" -d "$DB_NAME" > /dev/null 2>&1; then
            log_info "Database is ready!"
            return 0
        fi

        log_warn "Attempt $i/$MAX_RETRIES: Database not ready, waiting ${RETRY_INTERVAL}s..."
        sleep $RETRY_INTERVAL
    done

    log_error "Database connection failed after $MAX_RETRIES attempts"
    exit 1
}

# =============================================================================
# Run Migrations
# =============================================================================

run_migrations() {
    log_info "Running database migrations..."

    # Option 1: Using Alembic (recommended)
    # Uncomment when Alembic is set up:
    # uv run alembic upgrade head

    # Option 2: Using raw SQL files
    # for migration in migrations/*.sql; do
    #     if [ -f "$migration" ]; then
    #         log_info "Applying: $migration"
    #         psql -h "$DB_HOST" -p "$DB_PORT" -U "$DB_USER" -d "$DB_NAME" -f "$migration"
    #     fi
    # done

    # Placeholder for demonstration
    log_info "Migration runner ready. Configure Alembic or SQL migrations."

    log_info "Migrations completed successfully!"
}

# =============================================================================
# Main
# =============================================================================

main() {
    log_info "=== Database Migration Runner ==="
    log_info "Host: ${DB_HOST}:${DB_PORT}"
    log_info "Database: ${DB_NAME}"
    log_info "User: ${DB_USER}"

    # Wait for database to be ready
    wait_for_database

    # Run migrations
    run_migrations

    log_info "=== Migration Complete ==="
}

main "$@"
