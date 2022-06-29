.PHONY: po-update po-compile po release test update codex

po-update:
	python setup.py extract_messages
	python setup.py update_catalog

po-compile:
	python setup.py compile_catalog

po: po-update po-compile

release:
	python barrins_codex/card_list.py
	fullrelease

test:
	black barrins_codex/
	flake8 barrins_codex/
	pytest

update:
	pip install --upgrade pip
	pip install --upgrade --upgrade-strategy eager -e ".[dev]"

codex:
	black barrins_codex/
	flake8 barrins_codex/
	DEBUG=True codex
