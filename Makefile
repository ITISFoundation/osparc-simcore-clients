include ./scripts/common.Makefile

PYTHON_DIR    := $(CLIENTS_DIR)/python


.vscode/%.json: .vscode/%.template.json
	-$(if $(wildcard $@), \
	@echo "WARNING #####  $< is newer than $@ ####"; diff -uN $@ $<; false;,\
	@echo "WARNING ##### $@ does not exist, cloning $< as $@ ############"; cp $< $@)


.PHONY: info-api info-envs info-tools info-pip info

info-api: ## info on openapi specs
	# Openapi specs ---------
	@echo  ' title           : $(shell bash $(SCRIPTS_DIR)/jq.bash -r .info.title $(REPO_ROOT)/api/openapi.json)'
	@echo  ' version         : $(shell bash $(SCRIPTS_DIR)/jq.bash -r .info.version $(REPO_ROOT)/api/openapi.json)'


info-envs: ## info on envs
	# Environments ----------
	@echo ' CURDIR          : ${CURDIR}'
	@echo ' NOW_TIMESTAMP   : ${NOW_TIMESTAMP}'
	@echo ' VCS_URL         : ${VCS_URL}'
	@echo ' VCS_REF         : ${VCS_REF}'


info-tools: ## info on tooling
	# Tooling ---------------
	@echo ' awk           	 : $(shell awk -W version 2>&1 | head -n 1)'
	@echo ' curl	         : $(shell curl --version | head -n 1)'
	@echo ' docker        	 : $(shell docker --version)'
	@echo ' docker buildx 	 : $(shell docker buildx version)'
	@echo ' docker compose	 : $(shell docker compose version)'
	@echo ' jq            	 : $(shell jq --version)'
	@echo ' make          	 : $(shell make --version 2>&1 | head -n 1)'
	@echo ' python        	 : $(shell python3 --version)'
	@echo ' uv            	 : $(shell uv --version)'



info-pip: ## info index versions
	# Pypi ------------------
	@pip index versions \
		osparc \
		--pre \
		--index-url https://test.pypi.org/simple/ \
		--extra-index-url https://pypi.org/simple/


info: info-api info-envs info-tools info-pip ## all infos


.venv: .check-uv-installed
	@uv venv \
		--python 3.10 \
		$@
	## upgrading tools to latest version in $(shell python3 --version)
	@uv pip --quiet install --upgrade \
		pip~=24.0 \
		wheel \
		setuptools \
		uv
	@uv pip list


.PHONY: devenv
devenv: .venv .vscode/settings.json .vscode/launch.json ## create a python virtual environment with dev tools (e.g. linters, etc)
	@uv pip --quiet install -r requirements.txt
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

.PHONY: http-doc docs
docs: ## generate docs
	# generate documentation
	$(eval CLIENTS := $(shell ls clients))
	@for client in $(CLIENTS); do \
		echo "generating $${client} doc"; \
		pushd clients/$${client}; \
		make install-doc; \
		make docs; \
		popd; \
	done

http-doc: docs ## generates and serves doc
	# starting doc website
	@echo "Check site on http://127.0.0.1:50001/"
	python3 -m http.server 50001 --bind 127.0.0.1
