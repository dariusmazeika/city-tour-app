help:
	@echo 'make check-tools     - ensure pip-tools present in environment'
	@echo 'make compile         - compile requirements files'
	@echo 'make install         - install requirements/requirements.dev.txt'
	@echo 'make sync            - Compile and then install pip depenecys'
	@echo 'make mypy            - runs MyPy.'
	@echo 'make flake8          - runs Flake8'
	@echo 'make test            - runs tests.'
	@echo 'make check           - runs tests and other checks (Flake8 and MyPy). These checks should pass before pushing code.'
	@echo 'make makemigrations  - runs django makemigrations command.'
	@echo 'make migrate         - applies django migrations.'
	@echo 'make run             - starts django server at http://localhost:8000 for local development.'
	@echo 'make shell           - starts interactive django shell (all models are automatically imported).'

check-tools:
	pip install -U pip-tools

compile: check-tools
	pip-compile requirements/requirements.dev.in
	pip-compile requirements/requirements.in

install: check-tools
	pip-sync requirements/requirements.dev.txt

sync: compile install

mypy:
	mypy apps --config-file mypy.ini

flake8:
	pflake8 apps

test:
	pytest apps

check: flake8 mypy test

makemigrations:
	python manage.py makemigrations

migrate:
	python manage.py migrate

run:
	python manage.py runserver 0.0.0.0:8000

shell:
	python manage.py shell
