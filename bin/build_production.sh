#!/bin/bash

#builds production images

source bin/env.sh
./bin/build_static.sh
dcprod build --no-cache
