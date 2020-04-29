# vim:set noexpandtab :
.PHONY: help test install lint format

CURRENT_DIRECTORY=$(shell pwd)
VIRTUAL_ENV?=$(CURRENT_DIRECTORY)/venv
PIP?=${VIRTUAL_ENV}/bin/pip
PYTHON?=${VIRTUAL_ENV}/bin/python
BLACK?=${VIRTUAL_ENV}/bin/black
ISORT?=${VIRTUAL_ENV}/bin/isort
PYTEST=${VIRTUAL_ENV}/bin/pytest

.DEFAULT: help
help:
	@echo "make test"
	@echo "       run tests"
	@echo "make lint"
	@echo "       run black"

test:
	PYTHONPATH=$(CURRENT_DIRECTORY)/src ${PYTHON} -m pytest --cov=. --cov-config=.coveragerc --cov-report term-missing tests/ --junitxml=coverage-reports/test-report.xml --cov-report xml:coverage-reports/coverage-report.xml

install:
	python3 -m venv ${VIRTUAL_ENV}
	${PIP} install -r requirements.txt

lint: install
	${ISORT} --diff stax/*.py
	${BLACK} -t py37 --diff stax/

format: lint
	${ISORT} --apply stax/*.py
	${BLACK} -t py37 stax/

download-schema:
	curl --fail --compressed -s -o stax/data/schema.json https://api.au1.staxapp.cloud/20190206/public/api-document

bundle-test: install
	${PIP} install twine
	${PYTHON} setup.py sdist
	${VIRTUAL_ENV}/bin/twine check dist/*
	${VIRTUAL_ENV}/bin/twine upload --repository-url https://test.pypi.org/legacy/ dist/*