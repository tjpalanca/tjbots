# Platform 

PLATFORM ?= $(shell docker version --format '{{.Server.Os}}/{{.Server.Arch}}')

# Project

NAME := $(shell python3 -c 'import tomllib; print(tomllib.load(open("pyproject.toml", "rb"))["project"]["name"])')
VERSION := $(shell python3 -c 'import tomllib; print(tomllib.load(open("pyproject.toml", "rb"))["project"]["version"])')
REPO_URL := $(shell python3 -c 'import tomllib; print(tomllib.load(open("pyproject.toml", "rb"))["project"]["urls"]["Repository"])')
LICENSE := $(shell python3 -c 'import tomllib; print(tomllib.load(open("pyproject.toml", "rb"))["project"]["license"])')

# Environment

ENV ?= "sandbox"
SECRETS_DIR = /run/secrets
SECRETS_FILE = $(SECRETS_DIR)/tjbots.env
CACHE_DIR = ~/.cache

create:
	sudo mkdir -p $(SECRETS_DIR) && \
	sudo mkdir -p $(CACHE_DIR) && \
	sudo chown -R vscode:vscode $(CACHE_DIR) $(SECRETS_DIR) && \
	$(MAKE) deps && \
	$(MAKE) pre-commit-install 

start:
	op inject -f -i env/$(ENV).env -o $(SECRETS_FILE) && \
	op read "op://Development/Docker GitHub PAT/credential" | \
	docker login ghcr.io -u tjpalanca --password-stdin

clean: 
	rm -f .env && \
	rm -f /home/vscode/.docker/config.json

deps:
	uv sync --locked && \
	uv run playwright install --with-deps

# Docker

DOCKER_IMG=ghcr.io/tjpalanca/tjbots
DOCKER_COMPOSE := \
	REPO_URL=$(REPO_URL) \
	LICENSE=$(LICENSE) \
	VERSION=$(VERSION) \
	DOCKER_IMG=$(DOCKER_IMG) \
	DOCKER_NAME=$(NAME) \
	SECRETS_FILE=$(SECRETS_FILE) \
	docker compose -f build/docker-compose.yml

# Keep legacy targets for backward compatibility
docker-build: 
	$(DOCKER_COMPOSE) build

docker-push: 
	$(DOCKER_COMPOSE) push

docker-run: 
	$(DOCKER_COMPOSE) up

docker-up: 
	$(DOCKER_COMPOSE) up --detach

docker-down: 
	$(DOCKER_COMPOSE) down

docker-bash: 
	$(DOCKER_COMPOSE) exec $(NAME) /bin/bash

docker-publish:
	docker buildx build \
		--file build/Dockerfile \
		--platform $(PLATFORM) \
		--label "org.opencontainers.image.source=$(REPO_URL)" \
		--label "org.opencontainers.image.licenses=$(LICENSE)" \
		--tag $(DOCKER_IMG):$(VERSION) \
		--tag $(DOCKER_IMG):latest \
		--cache-to=type=registry,ref=$(DOCKER_IMG):cache,mode=max \
		--cache-from=type=registry,ref=$(DOCKER_IMG):cache \
		--push . 

# Testing

test:
	uv run pytest -v -s --log-cli-level=INFO

# Linting and formatting

lint:
	uv run ruff check .

format:
	uv run ruff format .

lint-fix:
	uv run ruff check --fix .

pre-commit-install:
	uv run pre-commit install

pre-commit-run:
	uv run pre-commit run --all-files

# Docs 

docs-build:
	cd docs && \
	uv run quartodoc build && \
	uv run quarto render

docs-preview: docs-build
	cd docs && \
	uv run quarto preview

docs-publish: docs-build
	cd docs && \
	uv run quarto publish gh-pages --no-render