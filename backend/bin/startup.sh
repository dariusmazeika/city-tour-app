#!/bin/bash
echo $DJANGO_SETTINGS_MODULE

if [[ $(expr match "${RUN_MODE:="DEVELOPMENT"}" "CELERY_") == 0 ]]; then
  python3 manage.py collectstatic --noinput
  python3 manage.py migrate -v 2 || exit 1
fi

if [[ $RUN_MODE == "QA" ]]; then
  python3 manage.py loaddata initial.json
  python3 manage.py createsuperuser --noinput
fi

if [[ $RUN_MODE != "GUNICORN" ]]; then
  if [[ $RUN_MODE == "CELERY_WORKER" ]]; then
    echo "Starting Celery worker"
    celery -A apps worker -l INFO -c 2
  elif [[ $RUN_MODE == "CELERY_BEAT" ]]; then
    echo "Starting Celery beat"
    celery -A apps beat -l INFO
  else
    echo "Starting Celery Worker and Celery Beat"
    celery -A apps worker -l INFO -c 2 &
    celery -A apps beat -l INFO
  fi
else
  echo "Starting Celery in detached mode"
  celery -A apps worker -l INFO --logfile celery.log --detach
  celery -A apps beat -l INFO --logfile celery_beat.log --detach
fi

if [[ $(expr match "$RUN_MODE" "CELERY_") == 0 ]]; then
  if [[ $RUN_MODE == "DEVELOPMENT" ]]; then
    python3 manage.py runserver 0.0.0.0:8000
  else
    gunicorn -b 0.0.0.0:8000 -c /app/gunicorn.conf.py wsgi:application
  fi
fi
