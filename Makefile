install:
	@poetry install

test:
	poetry run coverage run --source='.' manage.py test
	poetry run coverage json -o coverage.json

lint:
	poetry run flake8 task_manager

package-install:
	pip install --user dist/*.whl

build:
	poetry build

selfcheck:
	poetry check

preparetranslate:
	poetry run django-admin makemessages -l ru

translate:
	poetry run django-admin compilemessages

check: selfcheck test lint

.PHONY: install test lint selfcheck check build
