include ../scripts/common.Makefile


.PHONY: openapi-diff-dev.json
openapi-dev-diff.json: ## Diffs against newer openapi-dev.json and checks backwards compatibility
	$(SCRIPTS_DIR)/openapi-diff.bash \
	/specs/openapi.json \
	/specs/openapi-dev.json \
	--fail-on-incompatible \
	--json=/specs/$@



.PHONY: openapi-diff-dev.json
openapi-deploy-diff.json: ## Diffs against newer openapi-dev.json and checks backwards compatibility
	$(SCRIPTS_DIR)/openapi-diff.bash \
	https://api.osparc.io/api/v0/openapi.json \
	/specs/openapi.json \
	--fail-on-incompatible \
	--json=/specs/$@
