#!/bin/bash
echo $DJANGO_SETTINGS_MODULE

if [[ ${RUN_MODE:="DEVELOPMENT"} != "CELERY" ]]; then
	python3 manage.py migrate  -v 2 || exit 1
fi

if [[ $RUN_MODE == "QA" ]]; then
	python3 manage.py loaddata initial.json
fi

if [[ $DJANGO_SETTINGS_MODULE != "conf.settings_aws" ]]; then
	python3 manage.py collectstatic --noinput -v 2
fi

if [[ $RUN_MODE != "GUNICORN" ]]; then
	if [[ $RUN_MODE == "CELERY" ]]; then
		echo "Starting Celery"
		celery -A apps worker -Bl INFO -c 1
	else
		echo "Starting Celery in detached mode"
		celery -A apps worker -Bl INFO -c 4 --logfile /dev/stdout -D
	fi
fi

if [[ $RUN_MODE != "CELERY" ]]; then
	gunicorn -b 0.0.0.0:8000 -c /srv/gunicorn.conf.py wsgi:application
fi
