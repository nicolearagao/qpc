DATE		= $(shell date)
PYTHON		= $(shell which python)
PKG_VERSION = $(shell poetry -s version)
BUILD_DATE  = $(shell date +'%B %d, %Y')
QPC_VAR_PKG_SOURCE := $(or $(QPC_VAR_PKG_SOURCE), "qpc")
QPC_VAR_PKG_SOURCE_UPPER := $(shell echo $(QPC_VAR_PKG_SOURCE) | tr '[:lower:]' '[:upper:]')
CURRENT_YEAR=$(shell date +'%Y')

TOPDIR = $(shell pwd)
DIRS	= test bin locale src
PYDIRS	= quipucords
BINDIR  = bin

OMIT_PATTERNS = */test*.py,*/.virtualenvs/*.py,*/virtualenvs/*.py,.tox/*.py
pandoc = pandoc

help:
	@echo "Please use \`make <target>' where <target> is one of:"
	@echo "  help                to show this message"
	@echo "  install             to install the client egg"
	@echo "  clean               to remove client egg"
	@echo "  lint                to run all linters"
	@echo "  lint-ruff           to run the ruff linter"
	@echo "  lint-isort          to run the isort import order checker"
	@echo "  lint-black          to run the black format checker"
	@echo "  lint-docs           to run rstcheck against docs"
	@echo "  test                to run unit tests"
	@echo "  test-coverage       to run unit tests and measure test coverage"
	@echo "  manpage             to build the manpage"
	@echo "  build-container     to build the quipucords-cli container image"

clean:
	-rm -rf dist/ build/ qpc.egg-info/

install:
	$(PYTHON) setup.py build -f
	$(PYTHON) setup.py install -f

lint: lint-ruff lint-isort lint-black lint-docs

lint-ruff:
	poetry run ruff .

lint-isort:
	poetry run isort --check --diff .

lint-black:
	poetry run black --diff --check .

lint-docs:
	poetry run rstcheck docs/source/man.rst

test:
	poetry run pytest

test-coverage:
	poetry run pytest --cov=qpc
	poetry run coverage report --show-missing
	poetry run coverage xml

manpage:
	$(shell jinja -D QPC_VAR_CURRENT_YEAR $(CURRENT_YEAR) -X QPC_VAR docs/source/man.j2 -o docs/source/man.rst)
	$(pandoc) docs/source/man.rst \
	  --standalone -t man -o docs/$(QPC_VAR_PKG_SOURCE).1 \
	  --variable=section:1 \
	  --variable=date:'$(BUILD_DATE)' \
	  --variable=footer:'version $(PKG_VERSION)' \
	  --variable=header:'$(QPC_VAR_PKG_SOURCE_UPPER) Command Line Guide'

build-container:
	podman build -t quipucords-cli .
