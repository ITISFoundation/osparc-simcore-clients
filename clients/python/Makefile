-include ../../scripts/common.Makefile
PYTHON_DIR           := $(CLIENTS_DIR)/python
ARTIFACTS_DIR        := $(PYTHON_DIR)/artifacts
CONTAINER_API_JSON   := /local/$(REL_API_JSON_PATH)
GENERATOR            := python
UID                  := $(shell id -u)

.PHONY: artifacts_dir
artifacts_dir:
	-mkdir $(ARTIFACTS_DIR)

# Generation of Python client
.PHONY: python-client
python-client: validate-api-specification artifacts_dir ## generate python client
	-rm -r $(ARTIFACTS_DIR)/client
	docker run --rm --user $(UID):$(UID)\
			--volume "$(REPO_ROOT):/local" \
			$(OPENAPI_GENERATOR_IMAGE) generate \
			--generator-name=$(GENERATOR) \
			--git-user-id=$(GIT_USER_ID) \
			--git-repo-id=$(GIT_CLIENT_REPO_ID) \
			--http-user-agent="osparc-api/$(APP_VERSION)/python" \
			--input-spec=$(CONTAINER_API_JSON) \
			--output=/local/clients/python/artifacts/client \
			--additional-properties=$(subst $(space),$(comma),$(strip $(ADDITIONAL_PROPS))) \
			--package-name=osparc \
			--release-note="Updated to $(APP_VERSION)"

.PHONY: python-client-from-templates
python-client-from-templates: validate-api-specification artifacts_dir ## generate python client using templates in a specified directory (usage: 'make python-client-from-templates path/to/templates')
	$(eval TEMPLATE_DIR := $(word 2, $(MAKECMDGOALS)))
	@echo "Using template-dir: $(TEMPLATE_DIR)"
	-rm -r $(ARTIFACTS_DIR)/client
	@docker run --rm --user $(UID):$(UID)\
			--volume "$(REPO_ROOT):/local" \
			--volume "$(TEMPLATE_DIR):/tmp/python_templates" \
			$(OPENAPI_GENERATOR_IMAGE) generate \
			--generator-name=$(GENERATOR) \
			--git-user-id=$(GIT_USER_ID) \
			--git-repo-id=$(GIT_CLIENT_REPO_ID) \
			--http-user-agent="osparc-api/$(APP_VERSION)/python" \
			--input-spec=$(CONTAINER_API_JSON) \
			--output=/local/clients/python/artifacts/client \
			--additional-properties=$(subst $(space),$(comma),$(strip $(ADDITIONAL_PROPS))) \
			--package-name=osparc \
			--release-note="Updated to $(APP_VERSION)" \
			--template-dir=/tmp/python_templates

.PHONY: generator-help
generator-help: ## help on client-api generator
	# generate help
	@docker run --rm $(OPENAPI_GENERATOR_IMAGE) help generate

## Tools for "postprocessing" generated documentation --------------------------------------------

.PHONY: _copy-tests
_copy-tests: ## Replace git tracked tests clients/python/test by the automatically generated docs (N.B. check that the docs make sense before commiting into git)
	@-rm -r $(PYTHON_DIR)/test
	@mkdir $(PYTHON_DIR)/test
	@cp $(ARTIFACTS_DIR)/client/test/* $(PYTHON_DIR)/test/

.PHONY: postprocess-generated-docs
postprocess-generated-docs:  ## converts selected markdowns into notebooks and adds them to the documentation
	@-mkdir artifacts/client/docs/code_samples
	$(eval markdowns := $(shell ls artifacts/client/docs/*Api.md))
	$(eval outputs := $(subst artifacts/client/docs/,artifacts/client/docs/code_samples/,$(markdowns:.md=.ipynb)))
	$(MAKE) $(outputs)

artifacts/client/docs/code_samples/%.ipynb:artifacts/client/docs/%.md
	# Removing link in markdown
	@sed -i "/\b$(notdir $@)\b/d" $<
	notedown $< >$@
	# Appending link to markdown
	@echo "[Download as $(notdir $@)]($(subst artifacts/,clients/python/artifacts/,$@) \":ignore title\")" >> $<

.PHONY: docs
docs: python-client postprocess-generated-docs ## generate the python client documentation

## PYTHON DEVELOPMENT  ------------------------------------------------------------------

_check_venv_active:
	# checking whether virtual environment was activated
	@python3 -c "import sys; assert sys.base_prefix!=sys.prefix"

.PHONY: install-dev
install-dev: _check_venv_active ## install packages for development
	pip install -r requirements/dev.txt

.PHONY: install-test
install-test: _check_venv_active install-dev ## install packages for testing client
	pip install -r $(ARTIFACTS_DIR)/client/test-requirements.txt
	pip install -e $(ARTIFACTS_DIR)/client/


.PHONY: pylint
pylint: _check_venv_active ## runs linter (only to check errors. SEE .pylintrc enabled)
	pylint --rcfile "$(PYTHON_DIR)/.pylintrc" -v "$(ARTIFACTS_DIR)/client"


.PHONY: test-dev
test-dev: _check_venv_active ## runs tests during development
	# runs tests for development (e.g w/ pdb)
	pytest -vv --exitfirst --failed-first --durations=10 --pdb --ignore=$(ARTIFACTS_DIR)/client $(PYTHON_DIR)

.PHONY: dist
dist: artifacts_dir ## builds distribution wheel
	# installs pypa/build
	python -m pip install build
    # Build a binary wheel and a source tarball
	python -m build --sdist --wheel --outdir $(ARTIFACTS_DIR)/dist/ $(ARTIFACTS_DIR)/client

.PHONY: dist-ci
dist-ci: python-client dist ## build wheel and tar ball in a single command

## DOCKER -------------------------------------------------------------------------------

.env: .env-template ## creates .env file from defaults in .env-devel
	$(if $(wildcard $@), \
	@echo "WARNING #####  $< is newer than $@ ####"; diff -uN $@ $<; false;,\
	@echo "WARNING ##### $@ does not exist, cloning $< as $@ ############"; cp $< $@)

.PHONY: image
image: ## builds image $(APP_NAME):$(APP_VERSION)
	docker build -f Dockerfile -t $(APP_NAME):$(APP_VERSION) $(CURDIR)

.PHONY: shell
shell: ## runs container and opens bash shell
	docker run -it $(APP_NAME):$(APP_VERSION) /bin/bash



# RELEASE -------------------------------------------------------------------------------

prod_prefix := v
_git_get_current_branch = $(shell git rev-parse --abbrev-ref HEAD)

# NOTE: be careful that GNU Make replaces newlines with space which is why this command cannot work using a Make function
_url_encoded_title = $(APP_VERSION)
_url_encoded_tag = $(prod_prefix)$(APP_VERSION)
_url_encoded_target = $(if $(git_sha),$(git_sha),master)
_prettify_logs = $$(git log \
		$$(git describe --match="$(prod_prefix)*" --abbrev=0 --tags)..$(if $(git_sha),$(git_sha),HEAD) \
		--pretty=format:"- %s")
define _url_encoded_logs
$(shell \
	scripts/url-encoder.bash \
	"$(_prettify_logs)"\
)
endef
_git_get_repo_orga_name = $(shell git config --get remote.origin.url | \
							grep --perl-regexp --only-matching "((?<=git@github\.com:)|(?<=https:\/\/github\.com\/))(.*?)(?=.git)")

.PHONY: .check-master-branch
.check-master-branch:
	@if [ "$(_git_get_current_branch)" != "master" ]; then\
		echo -e "\e[91mcurrent branch is not master branch."; exit 1;\
	fi

.PHONY: release
release pre-release: .check-master-branch ## Creates github release link. Usage: make release-prod git_sha=optional
	# ensure tags are up-to-date
	@git pull --tags
	@echo -e "\e[33mOpen the following link to create a release:";
	@echo -e "\e[32mhttps://github.com/$(_git_get_repo_orga_name)/releases/new?prerelease=$(if $(findstring pre-, $@),1,0)&target=$(_url_encoded_target)&tag=$(_url_encoded_tag)&title=$(_url_encoded_title)&body=$(_url_encoded_logs)";
	@echo -e "\e[33mOr open the following link to create a release and paste the logs:";
	@echo -e "\e[32mhttps://github.com/$(_git_get_repo_orga_name)/releases/new?prerelease=$(if $(findstring pre-, $@),1,0)&target=$(_url_encoded_target)&tag=$(_url_encoded_tag)&title=$(_url_encoded_title)";
	@echo -e "\e[34m$(_prettify_logs)"
