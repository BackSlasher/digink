.PHONY: lint test

lint:
	venv/bin/python -m mypy .
	venv/bin/python -m black .
	venv/bin/python -m pylint $$(find digink -name '*.py')
