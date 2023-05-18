MANAGE := FLASK_APP=run.py

.PHONY: help
help: ## Show this help
	@egrep -h '\s##\s' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

.PHONY: venv
venv: ## Make a new virtual environment
	pipenv shell

.PHONY: install
install: venv ## Install or update dependencies
	pipenv install

initdb: ## Init and create database
	$(MANAGE) flask db init && $(MANAGE) flask init_db

migrate: ## Generate an initial migration
	$(MANAGE) flask db migrate -m 'Intial Migration'

upgrade: ## Apply the upgrade to the database
	$(MANAGE) flask db upgrade

shell: ## Flask Shell Load
	$(MANAGE) flask shell

test-cov: ## Run the coverage
	coverage run -m unittest discover

report-cov: ## Generate a code coverage report
	coverage report -m

gen-html-cov: ## Generate an HTML report
	coverage html

.PHONY: kill-process
kill-process: ## Kill process the server
	sudo lsof -t -i tcp:5000 | xargs kill -9
