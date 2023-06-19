include ./scripts/common.Makefile

PYTHON_DIR    := $(CLIENTS_DIR)/python

.PHONY: info
info: ## general information
	# system
	@echo ' CURDIR           : ${CURDIR}'
	@echo ' NOW_TIMESTAMP    : ${NOW_TIMESTAMP}'
	@echo ' VCS_URL          : ${VCS_URL}'
	@echo ' VCS_REF          : ${VCS_REF}'
	# installed in .venv
	@which python
	@pip list
	# API
	@echo  ' title        : ' $(shell python $(SCRIPTS_DIR)/get_json_entry.py info.title $(REPO_ROOT)/api/openapi.json)
	@echo  ' version      : ' $(shell python $(SCRIPTS_DIR)/get_json_entry.py info.version $(REPO_ROOT)/api/openapi.json)
	# nox
	@echo nox --list-session


.venv:
	@python3 --version
	python3 -m venv $@
	## upgrading tools to latest version in $(shell python3 --version)
	$@/bin/pip3 --quiet install --upgrade \
		pip~=22.0 \
		wheel \
		setuptools
	@$@/bin/pip3 list --verbose

.PHONY: devenv
devenv: .venv ## create a python virtual environment with dev tools (e.g. linters, etc)
	$</bin/pip3 --quiet install -r requirements.txt
	# Installing pre-commit hooks in current .git repo
	@$</bin/pre-commit install
	@echo "To activate the venv, execute 'source .venv/bin/activate'"


## VERSION -------------------------------------------------------------------------------

.PHONY: version-patch version-minor version-major
version-patch: ## commits version with bug fixes (use tag=1 to release)
	$(_bumpversion)
version-minor: ## commits version with backwards-compatible API addition or changes (use tag=1 to release)
	$(_bumpversion)
version-major: ## commits version with backwards-INcompatible addition or changes (use tag=1 to release)
	$(_bumpversion)

define _bumpversion
	# upgrades as $(subst version-,,$@) version, commits and tags
	@bump2version --verbose --list $(if $(tag),--tag,) $(subst version-,,$@)
endef

## DOCUMENTATION ------------------------------------------------------------------------
.PHONY: http-doc
http-doc: ## serves doc
	# starting doc website
	@echo "Check site on http://127.0.0.1:50001/"
	python3 -m http.server 50001 --bind 127.0.0.1

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
