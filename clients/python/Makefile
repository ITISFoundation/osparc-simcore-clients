-include ../../scripts/common.Makefile

CLIENTS_PYTHON_DIR   := $(CLIENTS_DIR)/python
ARTIFACTS_DIR        := $(CLIENTS_PYTHON_DIR)/artifacts
CONTAINER_API_JSON   := /local/$(OPENAPI_SPECS_JSON_REL_PATH)
GENERATOR            := python
UID                  := $(shell id -u)
ADDITIONAL_PROPS := \
	generateSourceCodeOnly=false\
	hideGenerationTimestamp=true\
	library=urllib3\
	packageName=osparc\
	packageUrl=$(shell bash $(SCRIPTS_DIR)/jq.bash -r .homepage $(REPO_ROOT)/api/config.json)\
	projectName=osparc_client
ADDITIONAL_PROPS := $(foreach prop,$(ADDITIONAL_PROPS),$(strip $(prop)))
VERSION_FILE := $(CLIENTS_PYTHON_DIR)/VERSION

.PHONY: generate_version
VERSION:
	@bash $(SCRIPTS_DIR)/generate_version.bash > $(VERSION_FILE)

.PHONY: artifacts_dir
artifacts_dir:
	-mkdir --parents $(ARTIFACTS_DIR)


# Generation of Python client
.PHONY: python-client
python-client: VERSION validate-api-specification artifacts_dir ## auto-generate python client
	$(eval VERSION := $(shell cat $(VERSION_FILE)))
	-rm -r $(ARTIFACTS_DIR)/client
	docker run --rm --user $(UID):$(UID)\
			--volume "$(REPO_ROOT):/local" \
			$(OPENAPI_GENERATOR_IMAGE) generate \
			--generator-name=$(GENERATOR) \
			--git-user-id=$(GIT_USER_ID) \
			--git-repo-id=$(GIT_CLIENT_REPO_ID) \
			--http-user-agent="osparc-api/$(VERSION)/python" \
			--input-spec=$(CONTAINER_API_JSON) \
			--output=/local/clients/python/artifacts/client \
			--additional-properties=packageVersion=$(VERSION),$(subst $(space),$(comma),$(strip $(ADDITIONAL_PROPS))) \
			--package-name=osparc_client \
			--release-note="Updated to $(VERSION)"
	$(MAKE) postprocess-build

.PHONY: python-client-from-templates
python-client-from-templates: VERSION validate-api-specification artifacts_dir ## generate python client using templates in a specified directory (usage: 'make python-client-from-templates -e TEMPLATE_DIR=path/to/templates')
	$(if $(TEMPLATE_DIR),,$(error The TEMPLATE_DIR environment variable must be set))
	@echo "Using template-dir: $(TEMPLATE_DIR)"
	$(eval VERSION := $(shell cat $(VERSION_FILE)))
	-rm -r $(ARTIFACTS_DIR)/client
	@docker run --rm --user $(UID):$(UID)\
			--volume "$(REPO_ROOT):/local" \
			--volume "$(TEMPLATE_DIR):/tmp/python_templates" \
			$(OPENAPI_GENERATOR_IMAGE) generate \
			--generator-name=$(GENERATOR) \
			--git-user-id=$(GIT_USER_ID) \
			--git-repo-id=$(GIT_CLIENT_REPO_ID) \
			--http-user-agent="osparc-api/$(VERSION)/python" \
			--input-spec=$(CONTAINER_API_JSON) \
			--output=/local/clients/python/artifacts/client \
			--additional-properties=packageVersion=$(VERSION),$(subst $(space),$(comma),$(strip $(ADDITIONAL_PROPS))) \
			--package-name=osparc_client \
			--release-note="Updated to $(VERSION)" \
			--template-dir=/tmp/python_templates
	$(MAKE) postprocess-build

.PHONY: generator-help
generator-help: ## help on client-api generator
	# generate help
	@docker run --rm $(OPENAPI_GENERATOR_IMAGE) help generate

## Tools for "postprocessing" generated documentation --------------------------------------------

ARTIFACTS_DOCS := artifacts/docs

.PHONY: docs
docs: artifacts_dir ## generate the python client documentation
	@-rm -rf $(ARTIFACTS_DOCS)
	@-mkdir $(ARTIFACTS_DOCS)
	$(eval notebooks := $(shell ls docs/*.ipynb))
	$(eval markdowns := $(subst docs/, $(ARTIFACTS_DOCS)/, $(notebooks:.ipynb=.md)))
	$(MAKE) $(markdowns)

artifacts/docs/%.md: docs/%.ipynb
	python -m nbconvert $< --to markdown --output-dir $(ARTIFACTS_DOCS)
	# Appending link to markdown
	@echo "[Download as $(notdir $<)]($(subst docs/,clients/python/docs/,$<) \":ignore title\")" >> $@



## PYTHON DEVELOPMENT  ------------------------------------------------------------------

_check_venv_active:
	# checking whether virtual environment was activated
	@python3 -c "import sys; assert sys.base_prefix!=sys.prefix"

.PHONY: install-dev
install-dev: _check_venv_active ## install packages for development
	pip install -r requirements/dev.txt

.PHONY: install-unit-test
install-unit-test: _check_venv_active ## install packages for unit testing client
	pip install -r $(CLIENTS_PYTHON_DIR)/requirements/unit-test.txt

.PHONY: install-e2e-test
install-e2e-test: _check_venv_active ## install packages for e2e testing client
	pip install -r $(CLIENTS_PYTHON_DIR)/requirements/e2e-test.txt

.PHONY: install-doc
install-doc: _check_venv_active install-dev ## install packages for generating documentation
	pip install -r $(CLIENTS_PYTHON_DIR)/requirements/doc.txt

.PHONY: pylint
pylint: _check_venv_active ## runs linter (only to check errors. SEE .pylintrc enabled)
	pylint --rcfile "$(CLIENTS_PYTHON_DIR)/.pylintrc" -v "$(ARTIFACTS_DIR)/client"

.PHONY: mypy
mypy: $(SCRIPTS_DIR)/mypy.bash $(CLIENTS_PYTHON_DIR)/mypy.ini ## runs mypy python static type-checker on this services's code. Use AFTER make install-*
	@$(SCRIPTS_DIR)/mypy.bash client

.PHONY: test-dev
test-dev: _check_venv_active ## runs tests during development
	# runs tests for development (e.g w/ pdb)
	python -m pytest \
		-vv \
		--exitfirst \
		--failed-first \
		--durations=10 \
		--pdb \
		$(CLIENTS_PYTHON_DIR)/test/test_osparc

.PHONY: dist
dist: artifacts_dir ## builds distribution wheel for `osparc_client` and `osparc` packages -> $(ARTIFACTS_DIR)/dist
	# installs pypa/build
	python -m pip install build
    # Build a binary wheel and a source tarball
	python -m build --sdist --wheel $(ARTIFACTS_DIR)/client
	python -m build --sdist --wheel $(CLIENTS_PYTHON_DIR)/src
	@-rm -rf $(ARTIFACTS_DIR)/dist
	@mkdir $(ARTIFACTS_DIR)/dist
	@cp $$(ls artifacts/client/dist/*.whl) $(ARTIFACTS_DIR)/dist
	@cp $$(ls client/dist/*.whl) $(ARTIFACTS_DIR)/dist
	@cp VERSION $(ARTIFACTS_DIR)/dist


.PHONY: build-n-install-osparc-dev
build-n-install-osparc-dev: python-client ## install the built osparc package in editable mode
	python -m pip install -e artifacts/client
	python -m pip install -e client/


.PHONY: postprocess-build
postprocess-build:
	black $(ARTIFACTS_DIR)/client/*.py
	@-rm -f $(ARTIFACTS_DIR)/client/README.md
	@echo "Please visit our [website](https://itisfoundation.github.io/osparc-simcore-clients/#/) for documentation" > $(ARTIFACTS_DIR)/client/README.md
	@-rm -rf $(CLIENTS_PYTHON_DIR)/src/osparc/data/
	@-mkdir $(CLIENTS_PYTHON_DIR)/src/osparc/data/
	@cp $(REPO_ROOT)/api/openapi.json $(CLIENTS_PYTHON_DIR)/src/osparc/data/


## TEST ---------------------------------------------------------------------------------

GH_TOKEN_FILE := $(wildcard $(HOME)/.gh-token)
ifneq ($(GH_TOKEN_FILE),)
	include $(GH_TOKEN_FILE)
endif
E2E_SHELL_DIR := /tmp/osparc-simcore-clients
USERID := $(shell id -u)
GROUPID := $(shell id -g)

.PHONY: e2e-shell
e2e-shell: guard-GH_TOKEN ## shell for running e2e tests
	@docker run \
		--user $(USERID):$(GROUPID) \
		--env GH_TOKEN=$(GH_TOKEN) \
		--volume $(REPO_ROOT):$(E2E_SHELL_DIR) \
		--workdir $(E2E_SHELL_DIR) \
		--entrypoint /bin/bash \
		-it \
		itisfoundation/osparc_python_tutorial_testing:v1 \
		-c "python -m venv /tmp/venv && source /tmp/venv/bin/activate && cd clients/python \
		&& make install-test && cd test/e2e && python ci/install_osparc_python_client.py && exec /bin/bash"


## DOCKER -------------------------------------------------------------------------------

.env: .env-template ## creates .env file from defaults in .env-devel
	$(if $(wildcard $@), \
	@echo "WARNING #####  $< is newer than $@ ####"; diff -uN $@ $<; false;,\
	@echo "WARNING ##### $@ does not exist, cloning $< as $@ ############"; cp $< $@)

.PHONY: image
image: VERSION ## builds image $(APP_NAME):version
	docker build -f Dockerfile -t $(APP_NAME):$(shell cat $(VERSION_FILE)) $(CURDIR)

.PHONY: shell
shell: VERSION ## runs container and opens bash shell
	docker run -it $(APP_NAME):$(shell cat $(VERSION_FILE)) /bin/bash
