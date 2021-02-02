.DEFAULT_GOAL := info
SHELL         := /bin/bash
VCS_URL       := $(shell git config --get remote.origin.url)
VCS_REF       := $(shell git rev-parse --short HEAD)
NOW_TIMESTAMP := $(shell date -u +"%Y-%m-%dT%H:%M:%SZ")
APP_NAME          = $(notdir $(CURDIR))
APP_VERSION    = $(shell python setup.py --version)


help: ## help on rule's targets
	@awk --posix 'BEGIN {FS = ":.*?## "} /^[[:alpha:][:space:]_-]+:.*?## / {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)


.PHONY: info
info:
	# system
	@echo ' CURDIR           : ${CURDIR}'
	@echo ' NOW_TIMESTAMP    : ${NOW_TIMESTAMP}'
	@echo ' VCS_URL          : ${VCS_URL}'
	@echo ' VCS_REF          : ${VCS_REF}'
	# installed in .venv
	@which python
	@pip list
	# package
	-@echo ' name         : ' $(shell python ${CURDIR}/setup.py --name)
	-@echo ' version      : ' $(shell python ${CURDIR}/setup.py --version)
	# nox
	@echo nox --list-session


## PYTHON DEVELOPMENT  ------------------------------------------------------------------

.PHONY: devenv

.env: .env-template ## creates .env file from defaults in .env-devel
	$(if $(wildcard $@), \
	@echo "WARNING #####  $< is newer than $@ ####"; diff -uN $@ $<; false;,\
	@echo "WARNING ##### $@ does not exist, cloning $< as $@ ############"; cp $< $@)


_check_venv_active:
	# checking whether virtual environment was activated
	@python3 -c "import sys; assert sys.base_prefix!=sys.prefix"

devenv: .venv
.venv: .env
	# creating virtual-env in $@
	@python3 -m venv $@
	@$@/bin/pip3 --quiet install --upgrade \
		pip \
		wheel \
		setuptools
	# installing tools
	@$@/bin/pip3 install -r requirements-tools.txt
	@echo "To activate the venv, execute 'source .venv/bin/activate'"


.PHONY: install-dev
install-dev: _check_venv_active 
	pip install -r requirements-tests.txt
	pip install -e .


.PHONY: test-dev
test-dev: _check_venv_active
	# runs tests for development (e.g w/ pdb)
	pytest -vv --exitfirst --failed-first --durations=10 --pdb $(CURDIR)


## NOTEBOOKS -----------------------------------------------------------------------------
.PHONY: notebooks

markdowns:=$(wildcard docs/md/*Api.md)
outputs:=$(subst docs/md,docs/md/code_samples,$(markdowns:.md=.ipynb))


notebooks: $(outputs)

# FIXME: should add a link in mds and REMOVE them from notebooks
docs/md/code_samples/%.ipynb:docs/md/%.md
	notedown $< >$@



## DOCUMENTATION ------------------------------------------------------------------------

.PHONY: serve-doc
serve-doc: # serves doc
	# starting doc website
	cd docs && python3 -m http.server 50001


# TODO: 
# - update README.md 
#	- from ## Documentation for API Endpoints to ## Author )
#   - all paths docs/ -> docs/md/
#   - copy to docs and replaces all docs/  -> md/
# - move all to docs/md
# - replace :\n``  -> :\n\n``
# - replace http://localhost https://api.osparc.io

## RELEASE -------------------------------------------------------------------------------

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


.PHONY: clean
clean:
	git clean -dxf -e .vscode


.PHONY: build
build:
	python setup.py sdist bdist_wheel


.PHONY: release
release: build # release by-hand (TEMP SOLUTION until FIXME: https://github.com/ITISFoundation/osparc-simcore-python-client/issues/16)
	python -m pip install twine
	python -m twine upload dist/*


## DOCKER -------------------------------------------------------------------------------


.PHONY: build
image:
	docker build -f Dockerfile -t $(APP_NAME):$(APP_VERSION) $(CURDIR)

.PHONY: shell
shell:
	docker run -it $(APP_NAME):latest /bin/bash