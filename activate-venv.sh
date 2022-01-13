#!/bin/bash

virtualenv .venv -p 3.10
source .venv/bin/activate

make install
make start-databases
