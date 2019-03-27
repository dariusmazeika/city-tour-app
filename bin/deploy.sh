#!/bin/bash

#builds production images,
#initializes database or creates db backup if it was initialized already
#(re)starts prodcution containers

source bin/env.sh

set -e
: ${DOCKER_CONFIG_PROD?"DOCKER_CONFIG_PROD not set"}

git pull
#for init_db.sh
export DOCKER_INIT_DB_CONFIG=$DOCKER_CONFIG_PROD

if [ "$EXTERNAL_DB" != "true" ]; then
  if  [ $(docker-compose -f docker-compose.yml -f $DOCKER_INIT_DB_CONFIG ps | grep db | wc -l) == 0 ]; then
    ./bin/init_db.sh
  else
    ./bin/backup.sh
  fi
else
  echo "Using external db"
fi

./bin/build_production.sh
./bin/stop_production.sh
./bin/start_production.sh
