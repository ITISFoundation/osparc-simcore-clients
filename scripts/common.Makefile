# Globals to be included into all Makefiles
# specification of the used openapi-generator-cli (see also https://github.com/ITISFoundation/openapi-generator)

.DEFAULT_GOAL := help

REPO_ROOT               := $(realpath $(dir $(abspath $(lastword $(MAKEFILE_LIST))))/..)
SCRIPTS_DIR             := $(REPO_ROOT)/scripts
CLIENTS_DIR             := $(REPO_ROOT)/clients
SHELL         := /bin/bash
VCS_URL       := $(shell git config --get remote.origin.url)
VCS_REF       := $(shell git rev-parse --short HEAD)
NOW_TIMESTAMP := $(shell date -u +"%Y-%m-%dT%H:%M:%SZ")
APP_NAME      := $(notdir $(CURDIR))
APP_VERSION   := $(shell bash $(SCRIPTS_DIR)/jq.bash -r .python.version $(REPO_ROOT)/api/config.json)

# Specify which openapi generator should be used to generate the clients in this repo
OPENAPI_GENERATOR_NAME  := itisfoundation/openapi-generator-cli-openapi-generator-v4.2.3
OPENAPI_GENERATOR_TAG   := v0
OPENAPI_GENERATOR_IMAGE := $(OPENAPI_GENERATOR_NAME):$(OPENAPI_GENERATOR_TAG)

# openapi specification
REL_API_JSON_PATH       := api/openapi.json
ABS_API_JSON_PATH       := $(REPO_ROOT)/$(REL_API_JSON_PATH)

GIT_USER_ID := ITISFoundation
GIT_CLIENT_REPO_ID := osparc-simcore-clients
GIT_OPENAPI_REPO_ID := openapi-generator
GENERATOR_NAME := python
ADDITIONAL_PROPS := \
	generateSourceCodeOnly=false\
	hideGenerationTimestamp=true\
	library=urllib3\
	packageName=osparc\
	packageUrl=$(shell bash $(SCRIPTS_DIR)/jq.bash -r .homepage $(REPO_ROOT)/api/config.json)\
	packageVersion=$(APP_VERSION)\
	projectName=osparc_client
ADDITIONAL_PROPS := $(foreach prop,$(ADDITIONAL_PROPS),$(strip $(prop)))

null  :=
space := $(null) #
comma := ,


help: ## help on rule's targets
	@awk --posix 'BEGIN {FS = ":.*?## "} /^[[:alpha:][:space:]_-]+:.*?## / {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)

# Validate openapi specification --------------------------------------------------------------

validate-api-specification: ## validates openapi-specification
	@docker run --rm \
			--volume "$(REPO_ROOT):/local" \
			$(OPENAPI_GENERATOR_IMAGE) validate --input-spec /local/$(REL_API_JSON_PATH)
