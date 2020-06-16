.DEFAULT_GOAL := info
SHELL := /bin/bash

# version control
VCS_URL       := $(shell git config --get remote.origin.url)
VCS_REF       := $(shell git rev-parse --short HEAD)
NOW_TIMESTAMP := $(shell date -u +"%Y-%m-%dT%H:%M:%SZ")


.PHONY: _check_venv_active
_check_venv_active:
	# checking whether virtual environment was activated
	@python3 -c "import sys; assert sys.base_prefix!=sys.prefix"


.venv:
	python3 -m venv $@
	$@/bin/pip3 --quiet install --upgrade \
		pip \
		wheel \
		setuptools

.PHONY: devenv
devenv: .venv 
	$</bin/pip3 install -r requirements.txt
	$</bin/pip3 install -r test-requirements.txt
	@echo "To activate the venv, execute 'source .venv/bin/activate'"


.PHONY: install-dev
install-dev: _check_venv_active
	pip install -e .


.PHONY: tests
tests: _check_venv_active
	pytest -v --pdb $(CURDIR)


.PHONY: info
info: 
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
clean:
	git clean -dxf -e .vscode

.PHONY: build
build: _check_venv_active clean 
	python setup.py sdist bdist_wheel

.PHONY: release
release: build
	python -m twine upload dist/*