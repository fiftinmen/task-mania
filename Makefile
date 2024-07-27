MANAGE := /root/.local/bin/poetry run python manage.py

PORT ?= 8000
.PHONY: start
start:
	/root/.local/bin/poetry run gunicorn --bind 0.0.0.0:$(PORT) task_manager.wsgi:application


.PHONY: build
build:
	./build.sh


.PHONY: dev
dev:
	/root/.local/bin/poetry run python manage.py runserver

.PHONY: test
test:
	/root/.local/bin/poetry run python manage.py test

.PHONY: setup
setup: db-clean install migrate

.PHONY: install
install:
	/root/.local/bin/poetry install

.PHONY: db-clean
db-clean:
	@rm db.sqlite3 || true

.PHONY: make-n-migrate
 make-n-migrate:
	@$(MANAGE) makemigrations
	@$(MANAGE) migrate

.PHONY: migrate
migrate:
	@$(MANAGE) migrate

.PHONY: shell
shell:
	@$(MANAGE) shell_plus --ipython

.PHONY: lint
lint:
	/root/.local/bin/poetry run flake8 task_manager

collectstatic:
	@$(MANAGE) collectstatic --noinput
