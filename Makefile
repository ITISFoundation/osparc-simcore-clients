
#
# GLOBALS
#

# defaults
.DEFAULT_GOAL := help

# Use bash not sh
SHELL := /bin/bash

# version control
VCS_URL       := $(shell git config --get remote.origin.url)
VCS_REF       := $(shell git rev-parse --short HEAD)
NOW_TIMESTAMP := $(shell date -u +"%Y-%m-%dT%H:%M:%SZ")
REPO_BASE_DIR := $(shell git rev-parse --show-toplevel)

# virtual env
VENV_DIR      := $(abspath $(REPO_BASE_DIR)/.venv)


#
# SUBTASKS
#

.PHONY: _check_venv_active
_check_venv_active:
	# checking whether virtual environment was activated
	@python3 -c "import sys; assert sys.base_prefix!=sys.prefix"


#
# MAIN RECIPES
#

.PHONY: devenv
.venv:
	python3 -m venv $@
	$@/bin/pip3 --quiet install --upgrade \
		pip \
		wheel \
		setuptools


devenv: .venv ## create a python virtual environment with dev tools (e.g. linters, etc)
	$</bin/pip3 install -r requirements.txt
	$</bin/pip3 install -r test-requirements.txt
	@echo "To activate the venv, execute 'source .venv/bin/activate'"


install-dev: _check_venv_active
	pip install -e .


.PHONY: tests
tests: _check_venv_active
	pytest -v $(CURDIR)



.PHONY: info
info: ## displays basic info
	# system
	@echo ' CURDIR           : ${CURDIR}'
	@echo ' NOW_TIMESTAMP    : ${NOW_TIMESTAMP}'
	@echo ' VCS_URL          : ${VCS_URL}'
	@echo ' VCS_REF          : ${VCS_REF}'
	# installed in .venv
	@pip list
	# package
	-@echo ' name         : ' $(shell python ${CURDIR}/setup.py --name)
	-@echo ' version      : ' $(shell python ${CURDIR}/setup.py --version)


.PHONY: clean
_GIT_CLEAN_ARGS = -dxf -e .vscode
clean: ## cleans all unversioned files in project and temp files create by this makefile
	# Cleaning unversioned
	@git clean -n $(_GIT_CLEAN_ARGS)
	@echo -n "Are you sure? [y/N] " && read ans && [ $${ans:-N} = y ]
	@echo -n "$(shell whoami), are you REALLY sure? [y/N] " && read ans && [ $${ans:-N} = y ]
	@git clean $(_GIT_CLEAN_ARGS)


.PHONY: help
# thanks to https://marmelab.com/blog/2016/02/29/auto-documented-makefile.html
help:
	@echo "usage: make [target] ..."
	@echo ""
	@echo "Targets for '$(notdir $(CURDIR))':"
	@echo ""
	@awk --posix 'BEGIN {FS = ":.*?## "} /^[[:alpha:][:space:]_-]+:.*?## / {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)
	@echo ""



