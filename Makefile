
VERSION := $(shell python -c 'import tomllib; print(tomllib.load(open("pyproject.toml", "rb"))["project"]["version"])')
REPO_URL := $(shell python -c 'import tomllib; print(tomllib.load(open("pyproject.toml", "rb"))["project"]["urls"]["Repository"])')
LICENSE := $(shell python -c 'import tomllib; print(tomllib.load(open("pyproject.toml", "rb"))["project"]["license"])')
DESCRIPTION := $(shell python -c 'import tomllib; print(tomllib.load(open("pyproject.toml", "rb"))["project"]["description"])')

# Application

APP_IMG=ghcr.io/tjpalanca/tjbots/app
APP_TAG=$(APP_IMG):$(VERSION)

app-build:
	docker build \
		-f app/Dockerfile \
		--label "org.opencontainers.image.source=$(REPO_URL)" \
		--label "org.opencontainers.image.description=\"$(DESCRIPTION)\"" \
		--label "org.opencontainers.image.licenses=$(LICENSE)" \
		-t $(APP_TAG) .

app-run: app-build
	docker run -it \
		-p 8080:8080 \
		$(APP_TAG)

app-bash: app-build
	docker run -it $(APP_TAG) /bin/bash

app-push: app-build
	docker push $(APP_TAG) && \
	docker tag $(APP_TAG) $(APP_IMG):latest && \
	docker push $(APP_IMG):latest