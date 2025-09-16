# Health Coach AI System - Makefile
# Provides convenient commands for development, testing, and deployment

.PHONY: help install dev test lint format clean build deploy docker-build docker-up docker-down

# Default target
.DEFAULT_GOAL := help

# Variables
PYTHON := python3
PIP := pip3
VENV := .venv
DOCKER_COMPOSE := docker-compose
PROJECT_NAME := health-coach

# Colors for output
GREEN := \033[0;32m
YELLOW := \033[0;33m
RED := \033[0;31m
NC := \033[0m # No Color

help: ## Show this help message
	@echo "$(GREEN)Health Coach AI System - Available Commands$(NC)"
	@echo "================================================"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "$(GREEN)%-20s$(NC) %s\n", $$1, $$2}'

# ============================================================================
# Development Environment
# ============================================================================

install: ## Install all dependencies
	@echo "$(YELLOW)Installing dependencies...$(NC)"
	$(PIP) install -r requirements.txt
	@echo "$(GREEN)Dependencies installed successfully$(NC)"

install-dev: ## Install development dependencies
	@echo "$(YELLOW)Installing development dependencies...$(NC)"
	$(PIP) install -r requirements.txt
	$(PIP) install pytest pytest-asyncio pytest-mock black isort flake8 mypy
	@echo "$(GREEN)Development dependencies installed successfully$(NC)"

venv: ## Create virtual environment
	@echo "$(YELLOW)Creating virtual environment...$(NC)"
	$(PYTHON) -m venv $(VENV)
	@echo "$(GREEN)Virtual environment created. Activate with: source $(VENV)/bin/activate$(NC)"

setup: venv install-dev ## Complete development environment setup
	@echo "$(YELLOW)Setting up development environment...$(NC)"
	cp .env.example .env
	mkdir -p data logs backups uploads
	@echo "$(GREEN)Development environment ready!$(NC)"
	@echo "$(YELLOW)Don't forget to:$(NC)"
	@echo "1. Edit .env with your API keys"
	@echo "2. Activate virtual environment: source $(VENV)/bin/activate"

# ============================================================================
# Development Commands
# ============================================================================

dev: ## Start development server with hot reload
	@echo "$(YELLOW)Starting development server...$(NC)"
	$(PYTHON) main.py --mode api --host 0.0.0.0 --port 8000

chat: ## Start interactive chat mode
	@echo "$(YELLOW)Starting chat interface...$(NC)"
	$(PYTHON) main.py --mode chat

chat-agent: ## Start chat with specific agent (Usage: make chat-agent AGENT=training_planner)
	@echo "$(YELLOW)Starting chat with $(AGENT) agent...$(NC)"
	$(PYTHON) main.py --mode chat --agent $(AGENT)

workflow: ## Run specific workflow (Usage: make workflow WORKFLOW=onboarding)
	@echo "$(YELLOW)Running $(WORKFLOW) workflow...$(NC)"
	$(PYTHON) main.py --mode workflow --workflow $(WORKFLOW)

# ============================================================================
# Testing
# ============================================================================

test: ## Run all tests
	@echo "$(YELLOW)Running tests...$(NC)"
	$(PYTHON) -m pytest tests/ -v

test-cov: ## Run tests with coverage report
	@echo "$(YELLOW)Running tests with coverage...$(NC)"
	$(PYTHON) -m pytest tests/ --cov=agents --cov=teams --cov=workflows --cov-report=html --cov-report=term

test-unit: ## Run unit tests only
	@echo "$(YELLOW)Running unit tests...$(NC)"
	$(PYTHON) -m pytest tests/unit/ -v

test-integration: ## Run integration tests only
	@echo "$(YELLOW)Running integration tests...$(NC)"
	$(PYTHON) -m pytest tests/integration/ -v

test-agents: ## Run agent-specific tests
	@echo "$(YELLOW)Running agent tests...$(NC)"
	$(PYTHON) -m pytest tests/agents/ -v

test-watch: ## Run tests in watch mode
	@echo "$(YELLOW)Running tests in watch mode...$(NC)"
	$(PYTHON) -m pytest tests/ -v --tb=short -x --ff

# ============================================================================
# Code Quality
# ============================================================================

lint: ## Run linting checks
	@echo "$(YELLOW)Running linting checks...$(NC)"
	flake8 agents/ teams/ workflows/ tools/ database/ config/ main.py
	mypy agents/ teams/ workflows/ tools/ database/ config/ main.py

format: ## Format code with black and isort
	@echo "$(YELLOW)Formatting code...$(NC)"
	black agents/ teams/ workflows/ tools/ database/ config/ main.py
	isort agents/ teams/ workflows/ tools/ database/ config/ main.py
	@echo "$(GREEN)Code formatted successfully$(NC)"

format-check: ## Check if code is properly formatted
	@echo "$(YELLOW)Checking code formatting...$(NC)"
	black --check agents/ teams/ workflows/ tools/ database/ config/ main.py
	isort --check-only agents/ teams/ workflows/ tools/ database/ config/ main.py

quality: format lint test ## Run all quality checks

# ============================================================================
# Database Management
# ============================================================================

db-init: ## Initialize database schema
	@echo "$(YELLOW)Initializing database...$(NC)"
	$(PYTHON) -c "from config.database_config import db_config; db_config.initialize_database()"
	@echo "$(GREEN)Database initialized successfully$(NC)"

db-migrate: ## Run database migrations
	@echo "$(YELLOW)Running database migrations...$(NC)"
	alembic upgrade head
	@echo "$(GREEN)Database migrations completed$(NC)"

db-seed: ## Seed database with sample data
	@echo "$(YELLOW)Seeding database with sample data...$(NC)"
	$(PYTHON) scripts/seed_database.py
	@echo "$(GREEN)Database seeded successfully$(NC)"

db-reset: ## Reset database (WARNING: destroys all data)
	@echo "$(RED)WARNING: This will destroy all data!$(NC)"
	@read -p "Are you sure? [y/N] " -n 1 -r; \
	if [[ $$REPLY =~ ^[Yy]$$ ]]; then \
		rm -f coach_dev.db health_coach.db; \
		$(MAKE) db-init; \
		echo "$(GREEN)Database reset completed$(NC)"; \
	fi

# ============================================================================
# Docker Commands
# ============================================================================

docker-build: ## Build Docker images
	@echo "$(YELLOW)Building Docker images...$(NC)"
	$(DOCKER_COMPOSE) build
	@echo "$(GREEN)Docker images built successfully$(NC)"

docker-up: ## Start all services with Docker Compose
	@echo "$(YELLOW)Starting services with Docker Compose...$(NC)"
	$(DOCKER_COMPOSE) up -d
	@echo "$(GREEN)Services started successfully$(NC)"

docker-down: ## Stop all Docker services
	@echo "$(YELLOW)Stopping Docker services...$(NC)"
	$(DOCKER_COMPOSE) down
	@echo "$(GREEN)Services stopped successfully$(NC)"

docker-logs: ## Show Docker container logs
	@echo "$(YELLOW)Showing container logs...$(NC)"
	$(DOCKER_COMPOSE) logs -f

docker-shell: ## Open shell in main application container
	@echo "$(YELLOW)Opening shell in application container...$(NC)"
	$(DOCKER_COMPOSE) exec health-coach /bin/bash

docker-clean: ## Clean up Docker resources
	@echo "$(YELLOW)Cleaning up Docker resources...$(NC)"
	$(DOCKER_COMPOSE) down -v --remove-orphans
	docker image prune -f
	docker volume prune -f
	@echo "$(GREEN)Docker cleanup completed$(NC)"

# ============================================================================
# Production Deployment
# ============================================================================

build: ## Build production package
	@echo "$(YELLOW)Building production package...$(NC)"
	$(PYTHON) setup.py sdist bdist_wheel
	@echo "$(GREEN)Production package built successfully$(NC)"

deploy-staging: ## Deploy to staging environment
	@echo "$(YELLOW)Deploying to staging...$(NC)"
	$(DOCKER_COMPOSE) -f docker-compose.staging.yml up -d
	@echo "$(GREEN)Deployed to staging successfully$(NC)"

deploy-prod: ## Deploy to production environment
	@echo "$(YELLOW)Deploying to production...$(NC)"
	@read -p "Are you sure you want to deploy to production? [y/N] " -n 1 -r; \
	if [[ $$REPLY =~ ^[Yy]$$ ]]; then \
		$(DOCKER_COMPOSE) -f docker-compose.prod.yml up -d; \
		echo "$(GREEN)Deployed to production successfully$(NC)"; \
	fi

# ============================================================================
# Monitoring and Maintenance
# ============================================================================

logs: ## Show application logs
	@echo "$(YELLOW)Showing application logs...$(NC)"
	tail -f logs/health_coach.log

health: ## Check system health
	@echo "$(YELLOW)Checking system health...$(NC)"
	curl -f http://localhost:8000/health || echo "$(RED)Health check failed$(NC)"

backup: ## Create system backup
	@echo "$(YELLOW)Creating system backup...$(NC)"
	mkdir -p backups
	$(DOCKER_COMPOSE) exec postgres pg_dump -U coach_user health_coach > backups/db-backup-$(shell date +%Y%m%d_%H%M%S).sql
	tar -czf backups/data-backup-$(shell date +%Y%m%d_%H%M%S).tar.gz data/
	@echo "$(GREEN)Backup created successfully$(NC)"

# ============================================================================
# Cleanup
# ============================================================================

clean: ## Clean up temporary files and caches
	@echo "$(YELLOW)Cleaning up temporary files...$(NC)"
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type d -name ".pytest_cache" -exec rm -rf {} +
	find . -type f -name ".coverage" -delete
	rm -rf htmlcov/
	rm -rf dist/
	rm -rf build/
	rm -rf *.egg-info/
	@echo "$(GREEN)Cleanup completed$(NC)"

clean-all: clean docker-clean ## Complete cleanup including Docker resources
	@echo "$(GREEN)Complete cleanup finished$(NC)"

# ============================================================================
# Documentation
# ============================================================================

docs: ## Generate documentation
	@echo "$(YELLOW)Generating documentation...$(NC)"
	mkdocs build
	@echo "$(GREEN)Documentation generated successfully$(NC)"

docs-serve: ## Serve documentation locally
	@echo "$(YELLOW)Serving documentation at http://localhost:8001$(NC)"
	mkdocs serve -a 0.0.0.0:8001

# ============================================================================
# Utility Commands
# ============================================================================

check-deps: ## Check for outdated dependencies
	@echo "$(YELLOW)Checking for outdated dependencies...$(NC)"
	$(PIP) list --outdated

update-deps: ## Update all dependencies
	@echo "$(YELLOW)Updating dependencies...$(NC)"
	$(PIP) install --upgrade -r requirements.txt
	@echo "$(GREEN)Dependencies updated successfully$(NC)"

env-check: ## Check environment configuration
	@echo "$(YELLOW)Checking environment configuration...$(NC)"
	@if [ -f .env ]; then \
		echo "$(GREEN)✓ .env file exists$(NC)"; \
	else \
		echo "$(RED)✗ .env file missing - copy from .env.example$(NC)"; \
	fi
	@$(PYTHON) -c "import sys; print(f'Python version: {sys.version}')"
	@$(PIP) --version

status: ## Show system status
	@echo "$(GREEN)Health Coach AI System Status$(NC)"
	@echo "=============================="
	@$(MAKE) env-check
	@$(MAKE) health