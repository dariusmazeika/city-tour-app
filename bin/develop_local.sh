#!/bin/bash
# Start all local structure without backend container

source bin/env.sh
./bin/init_db.sh
dcdev up --scale django=0
