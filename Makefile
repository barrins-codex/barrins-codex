.PHONY: release test update codex

compliance:
	isort barrins_codex/
	black barrins_codex/
	flake8 barrins_codex/

test:
	make compliance
	pytest

update:
	pip install --upgrade pip
	pip install --upgrade --upgrade-strategy eager -e ".[dev]"
	python barrins_codex/card_list.py

codex:
	make compliance
	DEBUG=True codex

release:
	python barrins_codex/card_list.py
	fullrelease
	make update
	make codex
