.PHONY: help install dev-install test test-cov lint format type-check security clean run docker-build docker-run setup pre-commit

# Default target
.DEFAULT_GOAL := help

# Variables
PYTHON := python3
PIP := $(PYTHON) -m pip
PYTEST := $(PYTHON) -m pytest
BLACK := $(PYTHON) -m black
ISORT := $(PYTHON) -m isort
FLAKE8 := $(PYTHON) -m flake8
MYPY := $(PYTHON) -m mypy
BANDIT := $(PYTHON) -m bandit

help: ## Show this help message
	@echo 'Usage: make [target]'
	@echo ''
	@echo 'Available targets:'
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-20s\033[0m %s\n", $$1, $$2}'

install: ## Install production dependencies
	$(PIP) install --upgrade pip
	$(PIP) install -r requirements.txt

dev-install: ## Install development dependencies
	$(PIP) install --upgrade pip
	$(PIP) install -r requirements.txt
	$(PIP) install pre-commit
	pre-commit install

setup: dev-install ## Complete development setup
	@echo "Creating necessary directories..."
	$(PYTHON) -c "from config import settings; settings.create_directories()"
	@echo "Setup complete! Run 'make help' to see available commands."

test: ## Run tests
	$(PYTEST) tests/ -v

test-cov: ## Run tests with coverage report
	$(PYTEST) tests/ --cov=. --cov-report=html --cov-report=term-missing
	@echo "Coverage report generated in htmlcov/index.html"

test-fast: ## Run tests without coverage (faster)
	$(PYTEST) tests/ -v -x

format: ## Format code with black and isort
	$(BLACK) . --line-length=100
	$(ISORT) . --profile black --line-length=100
	@echo "Code formatting complete!"

lint: ## Run flake8 linter
	$(FLAKE8) . --max-line-length=100 --extend-ignore=E203,E501,W503 --exclude=.git,__pycache__,build,dist,.eggs,venv

type-check: ## Run mypy type checker
	$(MYPY) . --ignore-missing-imports --no-strict-optional

security: ## Run security checks with bandit
	$(BANDIT) -r . -ll --exclude ./venv,./tests

quality: format lint type-check ## Run all code quality checks
	@echo "All quality checks passed!"

pre-commit: ## Run pre-commit hooks on all files
	pre-commit run --all-files

clean: ## Clean up generated files
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type f -name "*.coverage" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".mypy_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name "htmlcov" -exec rm -rf {} + 2>/dev/null || true
	@echo "Cleanup complete!"

clean-all: clean ## Clean everything including models and logs
	rm -rf models/* || true
	rm -rf Training_Logs/*.log || true
	rm -rf Prediction_Logs/*.log || true
	rm -rf Training_Database/* || true
	rm -rf Prediction_Database/* || true
	@echo "Deep cleanup complete!"

run: ## Run the Flask application
	$(PYTHON) main.py

run-dev: ## Run Flask in development mode
	FLASK_ENV=development DEBUG=True $(PYTHON) main.py

docker-build: ## Build Docker image
	docker build -t credit-card-default-prediction:latest .

docker-run: ## Run Docker container
	docker run -p 5000:5000 credit-card-default-prediction:latest

docker-stop: ## Stop all running containers
	docker stop $$(docker ps -q --filter ancestor=credit-card-default-prediction) || true

train: ## Trigger model training
	curl -X POST http://localhost:5000/train

predict: ## Trigger prediction
	curl -X POST http://localhost:5000/predict

check: format lint type-check test ## Run all checks (format, lint, type-check, test)
	@echo "✅ All checks passed successfully!"

ci: ## Run CI pipeline locally
	@echo "Running CI pipeline..."
	@make format
	@make lint
	@make type-check
	@make test-cov
	@echo "✅ CI pipeline completed successfully!"

.PHONY: docs
docs: ## Generate documentation (placeholder)
	@echo "Documentation generation not yet implemented"
	@echo "TODO: Add sphinx or mkdocs"

freeze: ## Update requirements.txt
	$(PIP) freeze > requirements.txt
	@echo "requirements.txt updated!"

upgrade: ## Upgrade all dependencies
	$(PIP) install --upgrade pip
	$(PIP) list --outdated --format=freeze | grep -v '^\-e' | cut -d = -f 1 | xargs -n1 $(PIP) install -U
	@echo "All dependencies upgraded!"

venv: ## Create virtual environment
	$(PYTHON) -m venv venv
	@echo "Virtual environment created. Activate with: source venv/bin/activate"

init: venv dev-install setup ## Initialize project from scratch
	@echo "✅ Project initialization complete!"
	@echo "Activate your virtual environment: source venv/bin/activate"
