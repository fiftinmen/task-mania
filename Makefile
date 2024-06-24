MANAGE := poetry run python manage.py

build:
	./build.sh

dev:
	poetry run python manage.py runserver

.PHONY: test
test:
	@poetry run pytest


.PHONY: test
test:
	@poetry run pytest


.PHONY: setup
setup: db-clean install migrate

.PHONY: install
install:
	@poetry install

.PHONY: db-clean
db-clean:
	@rm db.sqlite3 || true

.PHONY: make-n-migrate
makemigrations_and_migrate:
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
	@poetry run flake8 python_django_orm_blog
