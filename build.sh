#!/usr/bin/env bash

make install
make makem-n-migrate
poetry run python manage.py collectstatic --noinput