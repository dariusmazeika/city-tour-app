#!/bin/bash

#compile django dependencies
pip-compile requirements.in
pip-compile requirements.dev.in
