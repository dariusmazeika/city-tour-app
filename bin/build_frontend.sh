#!/bin/bash

#compile frontend production build to frontend/dist

source bin/env.sh

echo "building frontend..."
dcdev build
dcdev run --rm frontend npm run-script build
dcdev run --rm --no-deps django ./bin/collectstatic.sh
