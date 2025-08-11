PY = python3
PIP = $(PY) -m pip

.PHONY: venv install dev lint fmt type test ci

venv:
	$(PY) -m venv .venv
	. .venv/bin/activate

install:
	$(PIP) install -r requirements.txt

dev:
	$(PIP) install -r requirements.txt
	$(PIP) install -r requirements-dev.txt

lint:
	ruff check .

fmt:
	black .
	isort .

type:
	mypy src

test:
	pytest

ci: lint type test