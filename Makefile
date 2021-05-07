install:
	@poetry install

test:
	poetry run python manage.py test

lint:
	poetry run flake8 task_manager

package-install:
	pip install --user dist/*.whl

build:
	poetry build

selfcheck:
	poetry check

check: selfcheck test lint

.PHONY: install test lint selfcheck check build
