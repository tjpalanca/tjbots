# Platform 

PLATFORM ?= $(shell docker version --format '{{.Server.Os}}/{{.Server.Arch}}')

# Project

VERSION := $(shell python3 -c 'import tomllib; print(tomllib.load(open("pyproject.toml", "rb"))["project"]["version"])')
REPO_URL := $(shell python3 -c 'import tomllib; print(tomllib.load(open("pyproject.toml", "rb"))["project"]["urls"]["Repository"])')
LICENSE := $(shell python3 -c 'import tomllib; print(tomllib.load(open("pyproject.toml", "rb"))["project"]["license"])')

# Docker

DOCKER_IMG=ghcr.io/tjpalanca/tjbots
DOCKER_TAG=$(DOCKER_IMG):$(VERSION)
DOCKER_BUILD_ARGS=\
	--file Dockerfile \
	--platform $(PLATFORM) \
	--label "org.opencontainers.image.source=$(REPO_URL)" \
	--label "org.opencontainers.image.licenses=$(LICENSE)" \
	--tag $(DOCKER_TAG) \
	--tag $(DOCKER_IMG):latest 

docker-login:
	op read "op://Private/Docker GitHub PAT/credential" | \
	docker login ghcr.io -u tjpalanca --password-stdin

docker-publish:
	docker buildx build \
		$(DOCKER_BUILD_ARGS) \
		--cache-to=type=registry,ref=$(DOCKER_IMG):cache,mode=max \
		--cache-from=type=registry,ref=$(DOCKER_IMG):cache \
		--push . 

docker-build:
	docker build $(DOCKER_BUILD_ARGS) .

docker-push: 
	docker push $(DOCKER_TAG) && docker push $(DOCKER_IMG):latest

docker-run: app-build
	docker run \
		-p 8080:8080 \
		$(DOCKER_TAG)

docker-bash: app-build
	docker run -it $(DOCKER_TAG) /bin/bash

docker-bash:
	docker exec -it $(DOCKER_TAG) /bin/bash
