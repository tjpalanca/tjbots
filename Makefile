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
	op inject -f -i .devcontainer/devcontainer.env -o $(SECRETS_DIR)/devcontainer.env && \
	op inject -f -i envs/$(ENV).env -o $(SECRETS_FILE) && \
	op read "op://Development/Docker GitHub PAT/credential" | \
	docker login ghcr.io -u tjpalanca --password-stdin

clean: 
	rm -f .env && \
	rm -f /home/vscode/.docker/config.json

deps:
	uv sync --locked && \
	uv run playwright install --with-deps

# Docker 

DOCKER_IMG := ghcr.io/tjpalanca/tjbots
DOCKER_ENV := \
	DOCKER_NAME=$(NAME) \
	VERSION=$(VERSION) \
	DOCKER_IMG=$(DOCKER_IMG)

# Sandbox

SANDBOX_COMPOSE := \
    $(DOCKER_ENV) \
	SECRETS_FILE=$(SECRETS_FILE) \
	docker compose -f build/docker-compose.yml

sandbox-build:
	$(SANDBOX_COMPOSE) build

sandbox-push: 
	$(SANDBOX_COMPOSE) push

sandbox-run: 
	$(SANDBOX_COMPOSE) up

sandbox-up: 
	$(SANDBOX_COMPOSE) up --detach

sandbox-down: 
	$(SANDBOX_COMPOSE) down

sandbox-bash: sandbox-up
	$(SANDBOX_COMPOSE) exec app /bin/bash

# Production

PRODUCTION_SECRETS_FILE := $(PWD)/.env
PRODUCTION_COMPOSE := \
	$(DOCKER_ENV) \
	SECRETS_FILE=$(PRODUCTION_SECRETS_FILE) \
	docker compose -f build/docker-compose.yml --profile production -p $(NAME)

production-setup: 
	eval $$(op signin) && \
	op inject -i  envs/production.env -o $(PRODUCTION_SECRETS_FILE) --force 

production-up:
	$(PRODUCTION_COMPOSE) up --detach
 
production-down:
	$(PRODUCTION_COMPOSE) down

production-bash: 
	$(PRODUCTION_COMPOSE) exec app /bin/bash

# Building

BUILD_ENV := \
	$(DOCKER_ENV) \
	REPO_URL=$(REPO_URL) \
	LICENSE=$(LICENSE) 
BUILD_COMMAND := \
	cd build && \
	$(BUILD_ENV) \
	docker buildx bake --allow=fs.read=.. build

build-test:
	$(BUILD_COMMAND)

build-publish:
	$(BUILD_COMMAND) --push

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
