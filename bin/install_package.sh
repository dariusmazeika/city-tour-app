#!/bin/bash
package_name=$1
args=$2

#install new pyton package in django container
source bin/env.sh

if [[ -z $package_name ]]
then
    echo "specify package name"
    exit
fi

dcdev run --rm django pipenv install "$package_name"
