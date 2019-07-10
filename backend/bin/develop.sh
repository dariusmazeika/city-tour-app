#!/bin/bash
./bin/install.sh
python3 manage.py migrate
rm -f ./*.pid
celery -A apps worker -l info -c 4 --logfile celery.log -D
python3 manage.py runserver 0.0.0.0:8000