#!/usr/bin/env bash
apt update
apt install pipx
pipx install poetry
make install
make make-n-migrate
poetry run python manage.py collectstatic --noinput