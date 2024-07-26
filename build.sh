#!/usr/bin/env bash
export DEBIAN_FRONTEND=noninteractive
apt update -y
apt install pipx -y
pipx ensurepath
pipx install poetry
make install
make make-n-migrate
poetry run python manage.py collectstatic --noinput