#!/bin/bash
set -e

sed -i \
    -e "s/^DEBUG\s*=.*$/DEBUG = True/" \
    -e "s/^SECRET_KEY\s*=.*$/SECRET_KEY = '${SECRET_KEY}'/" \
    -e "s/^NEP_ORGANIZATION\s*=.*$/NEP_ORGANIZATION = '${NEP_ORGANIZATION}'/" \
    -e "s/^HMAC_SHARED_KEY\s*=.*$/HMAC_SHARED_KEY = '${HMAC_SHARED_KEY}'/" \
    -e "s/^HMAC_SECRET_KEY\s*=.*$/HMAC_SECRET_KEY = '${HMAC_SECRET_KEY}'/" \
    -e "s/^LOCATIONS\s*=.*$/LOCATIONS = {${LOCATIONS}}/" \
    -e "s/^GOOGLE_MAPS_API_KEY\s*=.*$/GOOGLE_MAPS_API_KEY = {${GOOGLE_MAPS_API_KEY}}/" \
    BurgersUnlimited/settings.py

build/cloudbuild/django/gunicorn-start.sh

exec "$@"
