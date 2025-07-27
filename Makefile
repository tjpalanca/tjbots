# Platform 

PLATFORM ?= $(shell docker version --format '{{.Server.Os}}/{{.Server.Arch}}')

# Project

VERSION := $(shell python3 -c 'import tomllib; print(tomllib.load(open("pyproject.toml", "rb"))["project"]["version"])')
REPO_URL := $(shell python3 -c 'import tomllib; print(tomllib.load(open("pyproject.toml", "rb"))["project"]["urls"]["Repository"])')
LICENSE := $(shell python3 -c 'import tomllib; print(tomllib.load(open("pyproject.toml", "rb"))["project"]["license"])')

# Application

APP_IMG=ghcr.io/tjpalanca/tjbots/app
APP_TAG=$(APP_IMG):$(VERSION)
APP_BUILD_ARGS=\
	--file app/Dockerfile \
	--platform $(PLATFORM) \
	--label "org.opencontainers.image.source=$(REPO_URL)" \
	--label "org.opencontainers.image.licenses=$(LICENSE)" \
	--tag $(APP_TAG) \
	--tag $(APP_IMG):latest

app-push:
	docker buildx build \
		$(APP_BUILD_ARGS) \
		--push . 

app-build:
	docker build $(APP_BUILD_ARGS) .

app-run: app-build
	docker run -it \
		-p 8080:8080 \
		$(APP_TAG)

app-bash: app-build
	docker run -it $(APP_TAG) /bin/bash
