# Variables
APP_NAME = tuya-alarm
DOCKER_IMAGE = $(APP_NAME):latest
PYTHON = venv/bin/python
PIP = venv/bin/pip
PYTEST = venv/bin/pytest
BLACK = venv/bin/black
FLAKE8 = venv/bin/flake8
COVERAGE = venv/bin/coverage
SAFETY = venv/bin/safety

.PHONY: help install install-dev run clean test test-coverage test-watch lint format format-check security check docker-build docker-run docker-stop compose-up compose-down compose-logs clean-test

help: ## Show this help message
	@echo 'Usage:'
	@echo '  make [target]'
	@echo ''
	@echo 'Targets:'
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-20s\033[0m %s\n", $$1, $$2}'

# Installation
install: ## Install production dependencies in virtual environment
	python3 -m venv venv
	$(PIP) install --upgrade pip
	$(PIP) install -r requirements.txt

install-dev: ## Install development dependencies
	python3 -m venv venv
	$(PIP) install --upgrade pip
	$(PIP) install -r requirements-dev.txt

# Running
run: ## Run the application locally
	$(PYTHON) main.py

# Testing
test: ## Run all tests
	$(PYTEST) tests/ -v

test-coverage: ## Run tests with coverage report
	$(PYTEST) tests/ \
		--cov=. \
		--cov-config=.coveragerc \
		--cov-report=html \
		--cov-report=term-missing \
		--cov-report=xml \
		-v

test-coverage-html: ## Run tests with HTML coverage report and open in browser
	$(PYTEST) tests/ \
		--cov=. \
		--cov-config=.coveragerc \
		--cov-report=html \
		-v
	@echo "Opening coverage report in browser..."
	@open htmlcov/index.html || xdg-open htmlcov/index.html || start htmlcov/index.html

test-watch: ## Run tests in watch mode (requires pytest-watch)
	$(PIP) install pytest-watch
	venv/bin/ptw tests/

test-failed: ## Run only failed tests from last run
	$(PYTEST) tests/ --lf -v

test-verbose: ## Run tests with extra verbose output
	$(PYTEST) tests/ -vv -s

# Code Quality
lint: ## Run flake8 linting
	@echo "Running flake8 linting..."
	$(FLAKE8) . --count --select=E9,F63,F7,F82 --show-source --statistics
	$(FLAKE8) . --count --exit-zero --max-complexity=10 --max-line-length=127 --statistics

format: ## Format code with black
	@echo "Formatting code with black..."
	$(BLACK) .

format-check: ## Check code formatting without making changes
	@echo "Checking code formatting..."
	$(BLACK) --check .

# Security
security: ## Run security checks with safety
	@echo "Running security checks..."
	$(SAFETY) check --json || true

# Combined checks
check: lint format-check test ## Run all checks (lint, format-check, test)
	@echo "All checks passed!"

check-coverage: lint format-check test-coverage ## Run all checks with coverage
	@echo "All checks with coverage passed!"

# Cleaning
clean: ## Remove virtual environment and cached files
	rm -rf venv
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

clean-test: ## Remove test and coverage artifacts
	rm -rf .pytest_cache
	rm -rf htmlcov
	rm -f .coverage
	rm -f coverage.xml

clean-all: clean clean-test ## Remove all generated files

# Docker
docker-build: ## Build Docker image
	docker build -t $(DOCKER_IMAGE) .

docker-run: ## Run Docker container
	docker run -p 5000:5000 --env-file .env $(DOCKER_IMAGE)

docker-stop: ## Stop all running containers for this image
	docker ps -q --filter ancestor=$(DOCKER_IMAGE) | xargs -r docker stop

docker-shell: ## Open shell in Docker container
	docker run -it --rm --env-file .env $(DOCKER_IMAGE) /bin/sh

docker-logs: ## Show Docker container logs
	docker logs -f $$(docker ps -q --filter ancestor=$(DOCKER_IMAGE))

# Docker Compose
compose-up: ## Run with docker-compose
	docker-compose up -d --build

compose-down: ## Stop docker-compose
	docker-compose down

compose-logs: ## View docker-compose logs
	docker-compose logs -f

compose-restart: ## Restart docker-compose services
	docker-compose restart

compose-shell: ## Open shell in docker-compose container
	docker-compose exec $(APP_NAME) /bin/sh

# Development helpers
dev: install-dev ## Setup development environment
	@echo "Development environment ready!"
	@echo "Run 'make test' to run tests"
	@echo "Run 'make run' to start the server"

requirements: ## Update requirements files
	$(PIP) freeze > requirements.txt

show-coverage: ## Show coverage report in terminal
	$(COVERAGE) report

show-routes: ## Show all Flask routes
	$(PYTHON) -c "from main import create_app; app = create_app(); print('\n'.join([str(rule) for rule in app.url_map.iter_rules()]))"