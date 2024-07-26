#!/usr/bin/env bash
apt update -y
apt install pipx -y
pipx install poetry
make install
make make-n-migrate
poetry run python manage.py collectstatic --noinput