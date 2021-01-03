SHELL := /bin/bash

.PHONY: help
help: ## Show this help
	@egrep -h '\s##\s' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

.PHONY: venv
venv: ## Make a new virtual environment
	python3 -m venv $(VENV) && source $(BIN)/activate

.PHONY: install
install: venv ## Make venv and install requirements
	$(BIN)/pip install -r requirements.txt

.PHONY: migrate
migrate: ## Make and run migrations
	python3 manage.py makemigrations
	python3 manage.py migrate

.PHONY: run
run: ## Run the Django server
	python3 manage.py runserver

.PHONY: shell
shell: ## Run the Django shell command
	python3 manage.py shell

start: install migrate run ## Install requirements, apply migrations, then start development server
