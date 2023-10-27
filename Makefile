.PHONY: all

all:
	@echo Please specify your command. Available commands: 'make test' or 'make validate'

test:
	 python -m unittest

validate:
	python -m pylint .\client
	python -m mypy .\client
	python -m flake8 .\client
