#!/bin/bash

#run django management command in development mode
source bin/env.sh

if [ "$PROD_MODE" != "true" ]; then
  dcdev run --rm  django python3 manage.py "$@"
else
  dcprod run --rm django python3 manage.py "$@"
fi
