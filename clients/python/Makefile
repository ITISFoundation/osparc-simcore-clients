
include ../../scripts/common.Makefile

PYTHON_DIR           := $(CLIENTS_DIR)/python
CONTAINER_API_JSON   := /local/$(REL_API_JSON_PATH)
GENERATOR            := python

python-client: validate-api-specification ## generate python client
	docker run --rm \
			--volume "$(REPO_ROOT):/local" \
			$(OPENAPI_GENERATOR_IMAGE) generate \
			--generator-name=$(GENERATOR) \
			--git-user-id=$(GIT_USER_ID) \
			--git-repo-id=$(GIT_CLIENT_REPO_ID) \
			--http-user-agent="osparc-api/$(APP_VERSION)/python" \
			--input-spec=$(CONTAINER_API_JSON) \
			--output=/local/clients/python \
			--additional-properties=$(subst $(space),$(comma),$(strip $(ADDITIONAL_PROPS))) \
			--package-name=osparc \
			--release-note="Updated to $(APP_VERSION)"

python-client-from-templates: validate-api-specification ## generate python client using templates in a specified directory
	$(eval TEMPLATE_DIR := $(word 2, $(MAKECMDGOALS)))
	@echo "Using template-dir: $(TEMPLATE_DIR)"
	@docker run --rm \
			--volume "$(REPO_ROOT):/local" \
			$(OPENAPI_GENERATOR_IMAGE) generate \
			--generator-name=$(GENERATOR) \
			--git-user-id=$(GIT_USER_ID) \
			--git-repo-id=$(GIT_CLIENT_REPO_ID) \
			--http-user-agent="osparc-api/$(APP_VERSION)/python" \
			--input-spec=$(CONTAINER_API_JSON) \
			--output=/local/clients/python \
			--additional-properties=$(subst $(space),$(comma),$(strip $(ADDITIONAL_PROPS))) \
			--package-name=osparc \
			--release-note="Updated to $(APP_VERSION)" \
			--template-dir $(TEMPLATE_DIR)

generator-help: ## help on client-api generator
	# generate help
	@docker run --rm $(OPENAPI_GENERATOR_IMAGE) help generate
