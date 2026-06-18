PY=python3

.PHONY: start build test lint format

start:
	@echo "Starting services via docker-compose..."
	docker-compose up --build

build:
	@echo "Building docker images"
	docker build -t biaslens-backend:local -f backend_deploy/Dockerfile backend_deploy
	docker build -t biaslens-frontend:local -f frontend/Dockerfile frontend

test:
	$(PY) -m pytest -q

lint:
	ruff check .

format:
	black .
