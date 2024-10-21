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

# Specify which openapi generator should be used to generate the clients in this repo
# Build from modified fork https://github.com/ITISFoundation/openapi-generator/tree/openapi-generator-v4.2.3
OPENAPI_GENERATOR_NAME  := itisfoundation/openapi-generator-cli-openapi-generator-v4.2.3
OPENAPI_GENERATOR_TAG   := v0
OPENAPI_GENERATOR_IMAGE := $(OPENAPI_GENERATOR_NAME):$(OPENAPI_GENERATOR_TAG)

# openapi specification
OPENAPI_SPECS_JSON_REL_PATH := api/openapi.json
OPENAPI_SPECS_JSON_ABS_PATH := $(REPO_ROOT)/$(OPENAPI_SPECS_JSON_REL_PATH)

GIT_USER_ID := ITISFoundation
GIT_CLIENT_REPO_ID := osparc-simcore-clients
GIT_OPENAPI_REPO_ID := openapi-generator
GENERATOR_NAME := python


null  :=
space := $(null) #
comma := ,


help: ## help on rule's targets
	@awk --posix 'BEGIN {FS = ":.*?## "} /^[[:alpha:][:space:]_-]+:.*?## / {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)


validate-api-specification: ## validates openapi-specification
	@docker run --rm \
			--volume "$(REPO_ROOT):/local" \
			$(OPENAPI_GENERATOR_IMAGE) validate --input-spec /local/$(OPENAPI_SPECS_JSON_REL_PATH)

#
# check variables: check that given variables are set and all have non-empty values,
# die with an error otherwise.
#
# Params:
#   1. Variable name(s) to test.
#   2. (optional) Error message to print.
guard-%:
	@ if [ "${${*}}" = "" ]; then \
		echo "Environment variable $* not set"; \
		exit 1; \
	fi

## CLEAN -------------------------------------------------------------------------------

.PHONY: clean-hooks
clean-hooks: ## Uninstalls git pre-commit hooks
	@-pre-commit uninstall 2> /dev/null || rm .git/hooks/pre-commit

_git_clean_args := -dx --force --exclude=.vscode --exclude=TODO.md --exclude=.venv --exclude=.python-version --exclude="*keep*"

.check-clean:
	@git clean -n $(_git_clean_args)
	@echo -n "Are you sure? [y/N] " && read ans && [ $${ans:-N} = y ]
	@echo -n "$(shell whoami), are you REALLY sure? [y/N] " && read ans && [ $${ans:-N} = y ]


clean: .check-clean ## cleans all unversioned files in project and temp files create by this makefile
	# Cleaning unversioned
	@git clean $(_git_clean_args)



.PHONY: .check-uv-installed
.check-uv-installed:
	@echo "Checking if 'uv' is installed..."
	@if ! command -v uv >/dev/null 2>&1; then \
			curl -LsSf https://astral.sh/uv/install.sh | sh; \
	else \
			printf "\033[32m'uv' is installed. Version: \033[0m"; \
			uv --version; \
	fi
	# upgrading uv
	-@uv self --quiet update
