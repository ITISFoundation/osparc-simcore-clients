.DEFAULT_GOAL := info
SHELL         := /bin/bash
VCS_URL       := $(shell git config --get remote.origin.url)
VCS_REF       := $(shell git rev-parse --short HEAD)
NOW_TIMESTAMP := $(shell date -u +"%Y-%m-%dT%H:%M:%SZ")

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




## PYTHON DEVELOPMENT

.venv:
	python3 -m venv $@
	$@/bin/pip3 --quiet install --upgrade \
		pip \
		wheel \
		setuptools
	$@/bin/pip3 install \
		nox \
		notedown \
		twine
	@echo "To activate the venv, execute 'source .venv/bin/activate'"


.PHONY: install-dev
install-dev:
	pip install -e .


.PHONY: tests
tests:
	# TODO: add here tests coverage
	pytest -v --pdb $(CURDIR)




## NOTEBOOKS
.PHONY: notebooks

markdowns:=$(wildcard docs/*Api.md)
outputs:=$(subst docs,code_samples,$(markdowns:.md=.ipynb))

notebooks: $(outputs)

# FIXME: should add a link in mds and REMOVE them from notebooks
docs/code_samples/%.ipynb:docs/%.md
	notedown $< >$@



## DOCUMENTATION

.PHONY: serve-doc
serve-doc:
	# starting doc website
	cd docs && python3 -m http.server 50001




## DEPLOYMENT

.PHONY: clean
clean:
	git clean -dxf -e .vscode


.PHONY: build
build: clean
	python setup.py sdist bdist_wheel


.PHONY: release
release: build
	python -m twine upload dist/*
