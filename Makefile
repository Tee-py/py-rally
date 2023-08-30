LINT_PATHS = py_rally/ tests/ conftest.py

lint:
	isort $(LINT_PATHS) --diff --check-only
	ruff $(LINT_PATHS)

format:
	isort $(LINT_PATHS)
	ruff $(LINT_PATHS) --fix
	black $(LINT_PATHS)

test:
	@echo "Running tests..."
	pytest --cov -s

publish:
	rm -rf dist/
	python3.9 -m poetry build
	twine upload dist/*