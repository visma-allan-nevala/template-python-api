#!/usr/bin/env bash
# =============================================================================
# Automated Setup Script
# =============================================================================
# This script sets up the development environment for this project.
#
# Usage:
#   ./setup.sh          # Full setup
#   ./setup.sh --quick  # Skip optional steps
# =============================================================================

set -e  # Exit on error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Print colored message
info() { echo -e "${BLUE}[INFO]${NC} $1"; }
success() { echo -e "${GREEN}[SUCCESS]${NC} $1"; }
warn() { echo -e "${YELLOW}[WARNING]${NC} $1"; }
error() { echo -e "${RED}[ERROR]${NC} $1"; exit 1; }

# =============================================================================
# Check Prerequisites
# =============================================================================

info "Checking prerequisites..."

# Check Python version
if ! command -v python3 &> /dev/null; then
    error "Python 3 is not installed. Please install Python 3.12+."
fi

PYTHON_VERSION=$(python3 -c 'import sys; print(f"{sys.version_info.major}.{sys.version_info.minor}")')
REQUIRED_VERSION="3.12"

if [[ "$(printf '%s\n' "$REQUIRED_VERSION" "$PYTHON_VERSION" | sort -V | head -n1)" != "$REQUIRED_VERSION" ]]; then
    error "Python $REQUIRED_VERSION+ is required. Found: $PYTHON_VERSION"
fi

success "Python $PYTHON_VERSION found"

# =============================================================================
# Install uv (if not present)
# =============================================================================

if ! command -v uv &> /dev/null; then
    info "Installing uv package manager..."
    curl -LsSf https://astral.sh/uv/install.sh | sh

    # Add uv to PATH for this session
    export PATH="$HOME/.cargo/bin:$PATH"

    if ! command -v uv &> /dev/null; then
        error "Failed to install uv. Please install manually: https://docs.astral.sh/uv/"
    fi
    success "uv installed successfully"
else
    success "uv is already installed"
fi

# =============================================================================
# Install Dependencies
# =============================================================================

info "Installing project dependencies..."
uv sync --extra dev
success "Dependencies installed"

# =============================================================================
# Generate Lock File
# =============================================================================

if [[ ! -f uv.lock ]]; then
    info "Generating uv.lock file for reproducible builds..."
    uv lock
    success "Lock file generated"
else
    info "Lock file already exists - running uv sync to ensure it's up to date"
    uv sync
fi

# =============================================================================
# Install Pre-commit Hooks
# =============================================================================

info "Installing pre-commit hooks..."
uv run pre-commit install
uv run pre-commit install --hook-type pre-push
success "Pre-commit hooks installed"

# =============================================================================
# Setup Environment File
# =============================================================================

if [[ ! -f .env ]]; then
    info "Creating .env file from .env.example..."
    cp .env.example .env
    success ".env file created - please update with your settings"
else
    warn ".env file already exists - skipping"
fi

# =============================================================================
# Quick Mode Check
# =============================================================================

if [[ "$1" != "--quick" ]]; then
    # Verify pre-commit hooks work
    info "Verifying pre-commit hooks..."
    uv run pre-commit run --all-files || warn "Some pre-commit checks failed (this is normal for a new project)"
fi

# =============================================================================
# Done!
# =============================================================================

echo ""
success "Setup complete!"
echo ""
info "Next steps:"
echo "  1. Update .env with your configuration"
echo "  2. Run 'make dev' to start the development server"
echo "  3. Visit http://localhost:8000/api/v1/health to verify"
echo "  4. Visit http://localhost:8000/docs for API documentation"
echo ""
info "Common commands:"
echo "  make dev        - Start development server"
echo "  make test       - Run tests"
echo "  make check      - Run linting and type checks"
echo "  make docker-up  - Start Docker services (Postgres, Redis)"
echo "  make help       - Show all available commands"
echo ""
