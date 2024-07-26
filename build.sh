#!/usr/bin/env bash
sudo apt update
sudo apt install pipx
pipx install poetry
make install
make make-n-migrate
poetry run python manage.py collectstatic --noinput