.PHONY: help build up down logs test lint

help:
	@echo "HeliosAI Makefile"
	@echo "Usage:"
	@echo "  make build    - Build all docker containers"
	@echo "  make up       - Start all services"
	@echo "  make down     - Stop all services"
	@echo "  make logs     - View logs of all services"
	@echo "  make test     - Run pytest locally"
	@echo "  make lint     - Run ruff and black"

build:
	docker-compose build

up:
	docker-compose up -d

down:
	docker-compose down

logs:
	docker-compose logs -f

test:
	python -m pytest tests/

lint:
	ruff check .
	black --check .
