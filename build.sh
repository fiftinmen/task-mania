#!/usr/bin/env bash
export DEBIAN_FRONTEND=noninteractive
export $PATH="/root/.local/bin:$PATH"
apt update -y
apt install pipx -y
pipx ensurepath
pipx install poetry
pipx run poetry install
make make-n-migrate
pipx run poetry run python manage.py collectstatic --noinput