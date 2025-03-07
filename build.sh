#!/usr/bin/env bash
export DEBIAN_FRONTEND=noninteractive
apt update -y
apt install pipx -y
pipx ensurepath
export PATH="/root/.local/bin:$PATH"    
pipx install poetry
export PATH="$HOME/.local/pipx/venvs/poetry/bin:$PATH"
make install
make make-n-migrate
make collectstatic