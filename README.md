# docker-django-webpack-starter

This is a starter project for a django app with webpack built frontend that uses docker for dev enironment.  
Docker and docker-compose is all you need to develop, build & deploy, run development or production mode with a single command.

## stack
python 3.7
node 10.7
Postgres latest
Django  2.2
Typescript
Webpack
Sass
Nginx 1.17
Gunicorn


## get started

Get latest docker & docker-compose:  
https://www.docker.com/  
https://docs.docker.com/compose/

Pull seed to your project:
```sh
git init
git remote add starter https://github.com/CornerCaseTechnologies/conercase-react-django-starter
git pull starter master
```

PyLint configuration file is in .pylintrc and the seed itself is configured to pass current PyLint configuration test without warnings. You can whether configure your IDE with this conf file or run PyLint manually:
```sh
pylint --output-format=parseable --rcfile=.pylintrc --load-plugins pylint_django backend > pylint.log
```

PEP8 configuration is in tox.ini and the seed itself is configured to pass current PEP8 analysis without warnings:
```sh
pycodestyle backend
```

Start dev server:
```sh
./bin/develop.sh
```
Wait for docker to set up container, then open [http://localhost:8000](http://localhost:8000)

After new python dependency add to requirements.txt on dev mode we need to run `docker-compose build` do build container.

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


#### enable ssl
Copy your .key and .crt files to `nginx/ssl` and run `./bin/deploy.sh`.

## install dependencies
```sh
# frontend
./bin/npm.sh install [package] --save-dev

# backend
./bin/pipinstall.sh [pacakge] #will also add entry to backend/requirements.txt
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
backend/templates/            - django global templates
backend/requirements.txt      - python dependencies
backend/gunicorn.conf.py      - gunicorn conf for production
backend/media/                - user uploads

logs/                         - in prod mode app, gunicorn, nginx, postgres logs go here
nginx/                        - nginx stuff for prod mode
nginx/ssl/                    - put key & cert here if you use ssl
nginx/nginx_nossl.conf        - nginx conf if no ssl is used
nginx/nginx_ssl.conf          - nginx conf for deploy with ssl
```
Frontend folder structure described in `frontend/README.MD`

## tests

```sh

# run tests
./bin/test.sh

# skip frontend build (eg, running tests repeatedly)
./bin/test.sh --skipbuild
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
-> set config to DB via `Enviroment variables` field. Available variables are:
'DB_NAME', 'DB_USER', 'DB_HOST', 'DB_PORT'. If using docker database from instructions above - 
DB_HOST=localhost;DB_PORT=9432; should be enough.
```

