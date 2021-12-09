#!/bin/bash

AUTH_TOKEN=$(curl -X 'POST' ${CI_ENVIRONMENT_URL::-7}/users/login/ -H 'Content-Type: application/json' -d '{"email": "test@test.com", "password": "test" }' | jq -r .token )
DAST_API_OVERRIDES_ENV='{ "headers": { "Authorization": "JWT '$AUTH_TOKEN'" }}'
