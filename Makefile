.PHONY: release test update codex

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

release:
	make test
	python barrins_codex/card_list.py
	fullrelease
	make update
	make codex
