# ============================================================================
# Environment management with uv, linting/formatting with ruff
# ============================================================================

.DEFAULT_GOAL := help

VENV := .venv
PYTHON := $(VENV)/bin/python
PIP := $(VENV)/bin/pip
PORT := 8060

# Project paths
SRC_DIR   := src
TESTS_DIR := tests
APP_ENTRY := src/dashtuto/app.py

# ============================================================================
# Environment
# ============================================================================
.PHONY: all install run test test-cov clean help

# Default: install and run
all: install run

.PHONY: install
install: ## Create venv and install all dependencies (including dev)
	uv sync --all-extras

.PHONY: lock
lock: ## Regenerate the lock file
	uv lock

.PHONY: upgrade
upgrade: ## Upgrade all dependencies to latest compatible versions
	uv lock --upgrade
	uv sync --all-extras

.PHONY: add
add: ## Add a dependency (usage: make add pkg=<package>)
	uv add $(pkg)

.PHONY: remove
remove: ## Remove a dependency (usage: make remove pkg=<package>)
	uv remove $(pkg)

# ============================================================================
# Code quality – Ruff
# ============================================================================

.PHONY: lint
lint: ## Run ruff linter
	uv run ruff check $(SRC_DIR) $(TESTS_DIR)

.PHONY: lint-fix
lint-fix: ## Run ruff linter with auto-fix
	uv run ruff check --fix $(SRC_DIR) $(TESTS_DIR)

.PHONY: format
format: ## Format code with ruff
	uv run ruff format $(SRC_DIR) $(TESTS_DIR)

.PHONY: format-check
format-check: ## Check formatting without modifying files
	uv run ruff format --check $(SRC_DIR) $(TESTS_DIR)

.PHONY: check
check: lint format-check ## Run all code quality checks (lint + format check)

.PHONY: fix
fix: lint-fix format ## Auto-fix lint issues and format code

# ============================================================================
# Run
# ============================================================================

.PHONY: run
run: $(VENV)/bin/activate
	@echo "🚀 Starting Dash app on http://localhost:$(PORT)"
	$(PYTHON) $(APP_ENTRY)
# ============================================================================
# Help
# ============================================================================


# Run tests
test: $(VENV)/bin/activate
	@echo "🧪 Running tests..."
	$(PYTHON) -m pytest tests/ -v

# Run tests with coverage
test-cov: $(VENV)/bin/activate
	@echo "🧪 Running tests with coverage..."
	$(PYTHON) -m pytest tests/ -v --cov=. --cov-report=html --cov-report=term-missing

# Clean everything
clean:
	rm -rf $(VENV) __pycache__ */__pycache__ */*/__pycache__ data/patients.json
	@echo "🧹 Cleaned!"

# Help
help:
	@echo "DashTuto - Dahs app following Dash documentation."
	@echo ""
	@echo "Usage:"
	@echo "  make          - Install and run"
	@echo "  make install  - Install dependencies in .venv"
	@echo "  make run      - Run the application"
	@echo "  make test     - Run unit tests"
	@echo "  make test-cov - Run tests with coverage"
	@echo "  make clean    - Remove .venv and cache"
	@echo "  make help     - Show this help"
