#!/usr/bin/env bash
export DEBIAN_FRONTEND=noninteractive
export $PATH="/root/.local/bin":$PATH
apt update -y
apt install pipx -y
pipx ensurepath
pipx ensurepath --prepend
pipx ensurepath --global
pipx install poetry
make install
make make-n-migrate
poetry run python manage.py collectstatic --noinput