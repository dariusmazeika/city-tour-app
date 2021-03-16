#!/bin/bash

# Stop on first error https://stackoverflow.com/a/3474556
set -e

echo "Backend checks"

echo "1. FlakeHell"
python3 -m flakehell lint

echo "2. MyPy"
python3 -m mypy apps --config-file mypy.ini

echo "3. Tests"
python3 -m pytest apps --cov --exitfirst --no-cov-on-fail

echo ""
echo "ALL CHECKS PASSED"
