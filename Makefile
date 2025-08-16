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

setup:
	sudo mkdir -p $(SECRETS_DIR) && \
	sudo mkdir -p $(CACHE_DIR) && \
	sudo chown -R vscode:vscode $(CACHE_DIR) $(SECRETS_DIR) && \
	uv sync --locked --no-install-project

start:
	op inject -f -i env/$(ENV).env -o $(SECRETS_FILE) && \
	op read "op://Development/Docker GitHub PAT/credential" | \
	docker login ghcr.io -u tjpalanca --password-stdin

clean: 
	rm -f .env && \
	rm -f /home/vscode/.docker/config.json

# Docker

DOCKER_IMG=ghcr.io/tjpalanca/tjbots
DOCKER_CACHE_IMG=$(DOCKER_IMG):cache
DOCKER_LATEST_IMG=$(DOCKER_IMG):latest
DOCKER_TAG=$(DOCKER_IMG):$(VERSION)
DOCKER_BUILD_ARGS=\
	--file build/Dockerfile \
	--platform $(PLATFORM) \
	--label "org.opencontainers.image.source=$(REPO_URL)" \
	--label "org.opencontainers.image.licenses=$(LICENSE)" \
	--tag $(DOCKER_TAG) \
	--tag $(DOCKER_IMG):latest 

docker-publish:
	docker buildx build \
		$(DOCKER_BUILD_ARGS) \
		--cache-to=type=registry,ref=$(DOCKER_CACHE_IMG),mode=max \
		--cache-from=type=registry,ref=$(DOCKER_CACHE_IMG) \
		--push . 

docker-build:
	docker build $(DOCKER_BUILD_ARGS) .

docker-push: 
	docker push $(DOCKER_TAG) && docker push $(DOCKER_LATEST_IMG)

DOCKER_NAME=$(NAME)
DOCKER_RUN_ARGS=\
	--rm \
	--mount type=bind,src=$(SECRETS_FILE),dst=$(SECRETS_FILE),ro \
	--publish 8080:8080 \
	--name $(DOCKER_NAME) \
	$(DOCKER_TAG)

docker-bash: 
	docker run -it $(DOCKER_RUN_ARGS) /bin/bash

docker-bash-in:
	docker exec -it $(DOCKER_NAME) /bin/bash

# Entrypoints

app-run: 
	docker run $(DOCKER_RUN_ARGS) 

# Docs 

docs-preview:
	cd docs && quarto preview