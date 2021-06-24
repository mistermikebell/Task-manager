install:
	@poetry install

test:
	poetry run coverage run --source='.' manage.py test
	poetry run coverage xml
	poetry run coverage report

lint:
	poetry run flake8 task_manager

package-install:
	pip install --user dist/*.whl

build:
	poetry build

selfcheck:
	poetry check

run:
	poetry run python manage.py

makemessages:
	poetry run django-admin makemessages -l ru

translate:
	poetry run django-admin compilemessages

check: selfcheck test lint

server:
	poetry run python manage.py runserver


.PHONY: install test lint selfcheck check build
