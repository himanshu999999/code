.PHONY: install install-web install-api install-worker dev dev-web dev-api dev-worker \
        docker-up docker-down docker-build test test-api test-worker lint seed evals clean

# Installation
install: install-web install-api install-worker

install-web:
	cd apps/web && npm install

install-api:
	cd services/api && pip install -r requirements.txt

install-worker:
	cd services/worker && pip install -r requirements.txt

# Development
dev: dev-web dev-api dev-worker

dev-web:
	cd apps/web && npm run dev

dev-api:
	cd services/api && uvicorn main:app --reload --host 0.0.0.0 --port 8000

dev-worker:
	cd services/worker && celery -A celery_app worker --loglevel=info

# Docker
docker-up:
	docker-compose up -d

docker-down:
	docker-compose down

docker-build:
	docker-compose build

docker-logs:
	docker-compose logs -f

# Testing
test: test-api test-worker

test-api:
	cd services/api && pytest tests/ -v

test-worker:
	cd services/worker && pytest tests/ -v

test-evals:
	python -m packages.evals.runner --dataset=sample_10 --dry-run

# Linting & Formatting
lint: lint-python lint-typescript

lint-python:
	flake8 services/ packages/
	black --check services/ packages/
	mypy services/ packages/

lint-typescript:
	cd apps/web && npm run lint

format: format-python format-typescript

format-python:
	black services/ packages/
	isort services/ packages/

format-typescript:
	cd apps/web && npm run format

# Database & Seeding
migrate:
	cd services/api && alembic upgrade head

seed:
	docker-compose exec api python -m app.services.seed_data

# Evaluation
evals:
	python -m packages.evals.runner --dataset=sample_50 --output=results/

evals-report:
	python -m packages.evals.runner --generate-report

# Cleanup
clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type d -name ".pytest_cache" -exec rm -rf {} +
	find . -type d -name "node_modules" -exec rm -rf {} +
	rm -rf apps/web/.next
	rm -rf results/

# Help
help:
	@echo "RepoPilot Makefile Commands"
	@echo ""
	@echo "Installation:"
	@echo "  make install          - Install all dependencies"
	@echo "  make install-web      - Install frontend dependencies"
	@echo "  make install-api      - Install API dependencies"
	@echo "  make install-worker   - Install worker dependencies"
	@echo ""
	@echo "Development:"
	@echo "  make dev              - Run all services locally"
	@echo "  make dev-web          - Run frontend only"
	@echo "  make dev-api          - Run API only"
	@echo "  make dev-worker       - Run worker only"
	@echo ""
	@echo "Docker:"
	@echo "  make docker-up        - Start all containers"
	@echo "  make docker-down      - Stop all containers"
	@echo "  make docker-build     - Build all containers"
	@echo "  make docker-logs      - View container logs"
	@echo ""
	@echo "Testing:"
	@echo "  make test             - Run all tests"
	@echo "  make test-api         - Run API tests"
	@echo "  make test-worker      - Run worker tests"
	@echo "  make test-evals       - Run evaluation dry-run"
	@echo ""
	@echo "Code Quality:"
	@echo "  make lint             - Run all linters"
	@echo "  make format           - Format all code"
	@echo ""
	@echo "Database:"
	@echo "  make migrate          - Run database migrations"
	@echo "  make seed             - Seed sample data"
	@echo ""
	@echo "Evaluation:"
	@echo "  make evals            - Run full evaluation suite"
	@echo "  make evals-report     - Generate evaluation report"
	@echo ""
	@echo "Cleanup:"
	@echo "  make clean            - Remove generated files"
