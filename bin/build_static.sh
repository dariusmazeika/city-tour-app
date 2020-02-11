#!/bin/bash

#compile static production build to static/dist

source bin/env.sh

echo "building static..."
dcdev build
dcdev run --rm --no-deps django ./bin/collectstatic.sh
