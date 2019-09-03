#!/bin/bash

#builds production images

source bin/env.sh
./bin/npm.sh i
./bin/build_frontend.sh
cp ./frontend/dist/assets.json ./backend/
dcprod build --no-cache
rm -f ./backend/assets.json
