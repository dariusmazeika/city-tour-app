#!/bin/bash

#builds production images

source bin/env.sh
./bin/npm.sh i
./bin/build_frontend.sh
cp ./frontend/dist/assets.json ./backend/
dcprod build
rm -f ./backend/assets.json
