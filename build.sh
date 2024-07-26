#!/usr/bin/env bash

make install
make make-n-migrate
poetry run python manage.py collectstatic --noinput