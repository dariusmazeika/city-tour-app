#!/bin/bash

#start development server on :8000

source bin/env.sh
./bin/init_db.sh
dcdev up --scale frontend=0
