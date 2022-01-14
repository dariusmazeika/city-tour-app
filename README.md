# Django REST framework

![Python](https://img.shields.io/badge/python-v3.10-informational)
![Postgres](https://img.shields.io/badge/postgres-14-informational)
![pip-tools](https://img.shields.io/badge/pip--tools-6.2.0-informational)
![Django](https://img.shields.io/badge/Django-latest-informational)
![DRF](https://img.shields.io/badge/DRF-latest-informational)
![Redis](https://img.shields.io/badge/Redis-latest-informational)
![OpenAPI](https://img.shields.io/badge/OpenAPI-v3-informational)

This is a starter project for a django REST app. Docker and docker-compose is all you need to develop, build, run development with a one liner.
Project To-Do's:
* Create Development environment `https://<domain>.cornercase.tech/admin/`
* Add master to protected branches, disable direct push
* Add CI pre-build image support to docker-compose.yml

## OpenAPI documentation

Documentation dynamically generated with OpenAPI3. It can be reached:

- `/schema/swagger/` for Swagger UI
- `/schema/redoc/` for ReDoc UI

## Get started
### I. Docker

For Mac users - install latest [Docker Desktop](https://docs.docker.com/desktop/mac/install/)
For non-mac install docker and docker-compose system.

Clone project and start using:

```sh
make run-docker
```

### II. Virtualenv (OSX)

```sh
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
brew install python@3.10

/usr/local/opt/python@3.10/bin/pip3 install virtualenv
/usr/local/opt/python@3.10/bin/python3 -m virtualenv .venv

source .venv/bin/activate
make sync
```

### III. GitPod
Project support gitpod integrations, to enable with gitlab follow - https://docs.gitlab.com/ee/integration/gitpod.html#enable-gitpod-in-your-user-settings

### Wrapped commands
Project is using `make` as universal wrapper. All most common commands are packed in
```shell script
$ make help
make check-tools     - ensure pip-tools present in environment
make compile         - compile requirements files
make install         - install requirements/requirements.dev.txt
make sync            - Compile and then install pip depenecys
make super           - Creates superuser with u:test@test.com, p:test.
make mypy            - runs MyPy.
make flake8          - runs Flake8
make test            - runs tests.
make check           - runs tests and other checks (Flake8 and MyPy). These checks should pass before pushing code.
make migrations      - runs django makemigrations command.
make migrate         - applies django migrations.
make run             - starts django server at http://localhost:8000 for local development.
make shell           - starts interactive django shell.
make ishell          - starts interactive django shell (all models are automatically imported).
make start-databases - starts redis and postgres in background
make down-docker     - stops docker containers and removes them
make purge-databases - stop postgres and purge data volume
make run-docker      - starts django docker environment
make pull-docker     - starts django docker environment (pull from CI registry)
make restore         - restores database.sql to docker-compose database
```

### Environment management
#### Using make command within docker
```shell script
$ make run-docker
/app $ make mypy
mypy apps --config-file mypy.ini
Success: no issues found in 57 source files
/app $ 
```
or oneliner (useful when images needs to be build from scratch)
```shell script
echo "make mypy" | make run-docker
```

#### Restoring database
CI has ability dump development databases for local debugging/testing. For quick restore of the database to docker-compose, from active python environment run:
```shell script
make restore         - restores database.sql to docker-compose database
```
#### Starting database containers
```shell script
make start-databases - starts redis and postgres in background
```

## Project dependencies

Dependencies are storied `requirements.in, requirements.dev.in` and managed by pip-tools.

## Environment variable mapping control
Environment variable mapping are controlled via `review-app-values.template.yaml`, more [details](https://kubernetes.io/docs/tasks/configure-pod-container/configure-pod-configmap/#configure-all-key-value-pairs-in-a-configmap-as-container-environment-variables) 

## tests locally (using Pycharm IDE)

```sh

# setup dependiecies 

create venv IDE project settings -> interpreter -> show all -> add (create somewhere outside project dir)
pip install -r requirements.txt
setup database if you have skipped creating docker based one from instructions above


# setup tests

run/debug configurations -> templates -> Django tests 
-> set path to tests `Custom settings` (usually `conf/settings_test.py`) 
-> set config to DB via `Enviroment variables` field. 
Available variables are - 'DB_NAME', 'DB_USER', 'DB_HOST', 'DB_PORT'. 
If using docker database from instructions above DB_HOST=localhost;DB_PORT=9432; should be enough.
Run tests from opened test file class or method by clicking on green arrow on the left 
or whole directory/app tests by right clicking on them from IDE project view -> Run:test
```

