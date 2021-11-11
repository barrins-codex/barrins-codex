.PHONY: po-update po-compile po release test update

po-update:
	python setup.py extract_messages
	python setup.py update_catalog

po-compile:
	python setup.py compile_catalog

po: po-update po-compile

release:
	fullrelease

test:
	black .
	flake8 .
	pytest

update:
	pip install --upgrade pip
	pip install --upgrade --upgrade-strategy eager -e ".[dev]"
