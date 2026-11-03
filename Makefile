.PHONY: run dev install lint test docker-up docker-down help

help:
	@echo ""
	@echo "  AI Research Report Agent — available commands"
	@echo ""
	@echo "  make install      Install dependencies"
	@echo "  make run          Start server (production)"
	@echo "  make dev          Start server with auto-reload"
	@echo "  make lint         Run ruff linter"
	@echo "  make test         Run pytest"
	@echo "  make docker-up    Build & start Docker containers"
	@echo "  make docker-down  Stop Docker containers"
	@echo ""

install:
	pip install -r requirements.txt

run:
	uvicorn main:app --host 0.0.0.0 --port 8000

dev:
	uvicorn main:app --host 0.0.0.0 --port 8000 --reload

lint:
	ruff check app/ main.py

test:
	pytest tests/ -v

docker-up:
	docker compose up --build

docker-down:
	docker compose down
