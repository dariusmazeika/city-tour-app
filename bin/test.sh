#!/bin/bash
source bin/env.sh

if [ -z "$SKIP_BUILD" ]; then
    ./bin/build_static.sh
else
    echo "skipping static build..."
fi

dctest run --rm  django ./bin/test.sh "$@"
