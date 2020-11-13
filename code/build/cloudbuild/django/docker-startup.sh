#!/bin/bash
set -e

sed -i \
    -e "s/^DEBUG\s*=.*$/DEBUG = True/" \
    -e "s/^SECRET_KEY\s*=.*$/SECRET_KEY = ['${SECRET_KEY}']/" \
    -e "s/^NEP_USERNAME\s*=.*$/NEP_USERNAME = '${NEP_USERNAME}'/" \
    -e "s/^NEP_PASSWORD\s*=.*$/NEP_PASSWORD = '${NEP_PASSWORD}'/" \
    -e "s/^NEP_APPLICATION_KEY\s*=.*$/NEP_APPLICATION_KEY = '${NEP_APPLICATION_KEY}'/" \
    -e "s/^NEP_ORGANIZATION\s*=.*$/NEP_ORGANIZATION = '${NEP_ORGANIZATION}'/" \
    -e "s/^NEP_SHARED_KEY\s*=.*$/NEP_SHARED_KEY = '${NEP_SHARED_KEY}'/" \
    -e "s/^HMAC_SHARED_KEY\s*=.*$/HMAC_SHARED_KEY = '${HMAC_SHARED_KEY}'/" \
    -e "s/^HMAC_SECRET_KEY\s*=.*$/HMAC_SECRET_KEY = '${HMAC_SECRET_KEY}'/" \
    -e "s/^CENSUS_API_KEY\s*=.*$/CENSUS_API_KEY = '${CENSUS_API_KEY}'/" \
    -e "s/^LOCATIONS\s*=.*$/LOCATIONS = {${LOCATIONS}}/" \
    BurgersUnlimited/settings.py

build/cloudbuild/django/gunicorn-start.sh

exec "$@"
