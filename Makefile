.PHONY: po-update po-compile po release

po-update:
	python setup.py extract_messages
	python setup.py update_catalog

po-compile:
	python setup.py compile_catalog

po: po-update po-compile

release:
	fullrelease

test:
	black barrins_codex
	flake8 barrins_codex
	pytest
