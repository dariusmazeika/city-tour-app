.PHONY: check-tools compile super install sync mypy flake8 test check migrations migrate run shell start-databases down-docker purge-databases run-docker restore ishell

help:
	@echo 'make check-tools     - ensure pip-tools present in environment'
	@echo 'make compile         - compile requirements files'
	@echo 'make install         - install requirements/requirements.dev.txt'
	@echo 'make sync            - Compile and then install pip depenecys'
	@echo 'make super           - Creates superuser with u:test@test.com, p:test.'
	@echo 'make mypy            - runs MyPy.'
	@echo 'make flake8          - runs Flake8'
	@echo 'make test            - runs tests.'
	@echo 'make check           - runs tests and other checks (Flake8 and MyPy). These checks should pass before pushing code.'
	@echo 'make migrations      - runs django makemigrations command.'
	@echo 'make migrate         - applies django migrations.'
	@echo 'make run             - starts django server at http://localhost:8000 for local development.'
	@echo 'make shell           - starts interactive django shell.'
	@echo 'make ishell          - starts interactive django shell (all models are automatically imported).'
	@echo 'make start-databases - starts redis and postgres in background'
	@echo 'make down-docker     - stops docker containers and removes them'
	@echo 'make purge-databases - stop postgres and purge data volume'
	@echo 'make run-docker      - starts django docker environment'
	@echo 'make pull-docker     - starts django docker environment (pull from CI registry)'
	@echo 'make restore         - restores database.sql to docker-compose database'

check-tools:
	pip install pip-tools==6.2.0 pip==21.2.4

compile: check-tools
	pip-compile requirements/requirements.dev.in
	pip-compile requirements/requirements.in

super:
	export DJANGO_SUPERUSER_EMAIL=test@test.com; export DJANGO_SUPERUSER_PASSWORD=test; python manage.py createsuperuser --noinput

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

migrations:
	python manage.py makemigrations

migrate:
	python manage.py migrate

run:
	python manage.py runserver 0.0.0.0:8000

shell:
	python manage.py shell

ishell:
	export DJANGO_SETTINGS_MODULE=conf.settings_test; python manage.py shell_plus --ipython

start-databases:
	docker-compose -f docker-compose.yml up -d postgres
	docker-compose -f docker-compose.yml up -d redis

down-docker:
	docker-compose -f docker-compose.yml down

purge-databases: down-docker
	docker-compose -f docker-compose.yml rm postgres -fv
	docker-compose -f docker-compose.yml rm redis -f

pull-docker:
	@echo "Login with gitlab credentials"
	docker login registry.gitlab.com
	docker-compose -f docker-compose.yml pull
	docker-compose -f docker-compose.yml run -p 8000:8000 django /bin/sh

run-docker:
	docker-compose -f docker-compose.yml run -p 8000:8000 django /bin/sh

restore:
	export PGPASSWORD=django; cat database.sql | psql -h 127.0.0.1 -p 9432 -U django
