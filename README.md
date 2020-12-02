# docker-django-webpack-starter

This is a starter project for a django app that uses docker for the environment.  
Docker and docker-compose is all you need to develop, build & deploy, run development or production mode with a single command.

## stack
python 3.8
Postgres latest
Django 3.1
Nginx 1.17
Gunicorn


## get started

Get latest docker & docker-compose:  
https://www.docker.com/  
https://docs.docker.com/compose/

Pull seed to your project:
```sh
git init
git remote add starter https://github.com/CornerCaseTechnologies/conercase-django-starter
git pull starter master
# Remove git history of a seed before starting a new project
rm -rf .git  
```

This project is Flakehell (flake8) and MyPy compatible and all checks can be launched via:
```shell script
cd backend
./bin/check.sh
```

Start dev server:
```sh
./bin/develop.sh
```
Wait for docker to set up container, then open [http://localhost:8000](http://localhost:8000)

For starting the whole structure just without backend container:
```sh
./bin/develop_local.sh
cd backend/
source .env-local
python manage.py runserver
```
This will start initially DB and redis container while letting you to start backend service locally in the host for easier debugging and development

### setup production server

1. install docker, docker-compose, git
2. add deploy key to git repo
3. clone repository, checkout appropriate branch
4. create `.env` file at project root with env vars, sample:
```sh
export DOCKER_CONFIG_PROD=docker-compose.production.yml #docker-compose file to use
export PROD_MODE=true # always true for production mode
```
5. run deploy script `./bin/deploy.sh`  

In prod mode sources are added to docker image rather than mounted from host. Nginx serves static files, proxy pass to gunicorn for django app. Logs in `logs` dir.

In case production environment uses external database, set env variable to not backup database:
```sh
export EXTERNAL_DB=true
```


## install dependencies
```sh
# backend
./bin/install_package.sh [package]
```

## backup & restore database

```sh
# create a backup in backups dir
./bin/backup.sh

# restore from a backup in backups dir (server must be stopped)
./bin/restore.sh backups/somebackup.bak
```

## run django management commands
```sh
#dev mode
./bin/django.sh [command]

#create migration
./bin/django.sh makemigrations myapp

```

## translations
```sh
# dump to fixture
./bin/django.sh dumpdata --indent 4 --natural-primary translations > backend/apps/translations/fixtures/initial.json

# load from fixture
./bin/django.sh loaddata initial.json
```

## layout

```
bin/                          - various utility scripts

docker-compose.yml            - base docker compose config
docker-compose.production.yml - production docker compose config

backend/                      - backend stuff
backend/apps/                 - django apps
backend/conf/                 - django settings files
backend/conf/settings.py      - default config
backend/conf/settings_prod.py - production config
backend/conf/settings_aws.py  - production config for AWS env
backend/conf/settings_qa.py   - config for review app env
backend/gunicorn.conf.py      - gunicorn conf for production
backend/media/                - user uploads

logs/                         - in prod mode app, gunicorn, nginx, postgres logs go here
nginx/                        - nginx stuff for prod mode
nginx/nginx.conf              - nginx conf
```

## tests

```sh

# run tests
./bin/test.sh
```

## tests locally (using Pycharm IDE)

```sh

# setup dependiecies 

create venv IDE project settings -> interpreter -> show all -> add (create somewhere outside project dir)
pip install -r requirements.txt
setup database if you have skipped creating docker based one from instructions above


# setup tests

run/debug configurations -> templates -> Django tests 
-> set path to tests `Custom settings` (usually `/backend/conf/settings_test.py`) 
-> set config to DB via `Enviroment variables` field. 
Available variables are - 'DB_NAME', 'DB_USER', 'DB_HOST', 'DB_PORT'. 
If using docker database from instructions above DB_HOST=localhost;DB_PORT=9432; should be enough.
Run tests from opened test file class or method by clicking on green arrow on the left 
or whole directory/app tests by right clicking on them from IDE project view -> Run:test
```

