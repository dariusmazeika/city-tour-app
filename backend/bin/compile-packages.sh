#!/bin/bash

#install django dependencies
pip-compile requirements.in
pip-compile requirements.dev.in
