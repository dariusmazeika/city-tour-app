#!/bin/bash
source bin/env.sh

dcdeploy run django bin/test.sh "$@"
