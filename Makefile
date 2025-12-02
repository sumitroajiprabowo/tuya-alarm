# Variables
APP_NAME = tuya-alarm
DOCKER_IMAGE = $(APP_NAME):latest
PYTHON = venv/bin/python
PIP = venv/bin/pip

.PHONY: help install run clean docker-build docker-run

help: ## Show this help message
	@echo 'Usage:'
	@echo '  make [target]'
	@echo ''
	@echo 'Targets:'
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-20s\033[0m %s\n", $$1, $$2}'

install: ## Install dependencies in virtual environment
	python3 -m venv venv
	$(PIP) install -r requirements.txt

run: ## Run the application locally
	$(PYTHON) main.py

clean: ## Remove virtual environment and cached files
	rm -rf venv
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

docker-build: ## Build Docker image
	docker build -t $(DOCKER_IMAGE) .

docker-run: ## Run Docker container
	docker run -p 5050:5050 --env-file .env $(DOCKER_IMAGE)

docker-stop: ## Stop all running containers for this image
	docker ps -q --filter ancestor=$(DOCKER_IMAGE) | xargs -r docker stop

compose-up: ## Run with docker-compose
	docker-compose up -d --build

compose-down: ## Stop docker-compose
	docker-compose down

compose-logs: ## View docker-compose logs
	docker-compose logs -f
