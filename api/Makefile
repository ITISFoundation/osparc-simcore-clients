include ../scripts/common.Makefile


define download_openapi
	@curl -L $(1) -o $(2) || (echo "Failed to download $(2)" && exit 1)
endef

.PHONY: openapi-master.json
openapi-master.json:
	$(call download_openapi, https://raw.githubusercontent.com/ITISFoundation/osparc-simcore-clients/refs/heads/master/api/openapi.json,$@)

.PHONY: openapi-deploy.json
openapi-deploy.json:
	$(call download_openapi, https://api.osparc.io/api/v0/openapi.json,$@)


define openapi_diff
	$(SCRIPTS_DIR)/openapi-diff.bash $(1) /specs/openapi.json \
		--fail-on-incompatible \
		--json="/specs/$(2)"
endef


.PHONY: openapi-master-diff.json
openapi-master-diff.json: ## Diffs against newer openapi-dev.json and checks backwards compatibility
	$(call openapi_diff, https://raw.githubusercontent.com/ITISFoundation/osparc-simcore-clients/refs/heads/master/api/openapi.json,$@)


.PHONY: openapi-deploy-diff.json
openapi-deploy-diff.json: ## Diffs against newer openapi-dev.json and checks backwards compatibility
	$(call openapi_diff, https://api.osparc.io/api/v0/openapi.json,$@)


.PHONY: openapi-osparc-simore-master-branch
openapi-osparc-simore-master-branch: ## recover form osparc-smicore repo master branch
	$(call download_openapi, https://raw.githubusercontent.com/ITISFoundation/osparc-simcore/refs/heads/master/services/api-server/openapi.json,openapi.json)