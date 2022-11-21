help:                             ## Display a help message detailing commands and their purpose
	@echo "Commands:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'
	@echo ""

## [DEV ENV SETUP]
install-docker-ubuntu:            ## installs docker and docker-compose on Ubuntu
	sudo apt-get remove docker docker-engine docker.io containerd runc
	sudo apt-get update
	sudo apt-get -y install apt-transport-https ca-certificates curl gnupg-agent software-properties-common
	curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
	sudo apt-key fingerprint 0EBFCD88
	sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(shell lsb_release -cs) stable" || { echo "$(shell lsb_release -cs) is not yet supported by docker.com."; exit 1; }
	sudo apt-get update
	sudo apt-get install -y docker-ce gettext
	sudo curl -L "https://github.com/docker/compose/releases/download/v2.2.3/docker-compose-$(shell uname -s)-$(shell uname -m)" -o /usr/local/bin/docker-compose
	sudo chmod +x /usr/local/bin/docker-compose

install-docker-macos:             ## installs homebrew (you can skip this at runtime), docker and docker-compose on MacOS
	/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
	brew update
	brew cask install docker
	brew install docker-compose gettext

build:                            ## builds the container for production
	ENVIRONMENT=production docker-compose up -d --build --force-recreate --remove-orphans

build-dev:                        ## builds the container with the development flag
	ENVIRONMENT=development docker-compose up -d --build --force-recreate --remove-orphans

build-stage:                      ## builds the container with the staging flag
	ENVIRONMENT=staging docker-compose up -d --build --force-recreate --remove-orphans

superuser:                        ## creates a superuser for the API
	docker-compose exec paul ./paul_api/manage.py createsuperuser

adminshell:                        ## opens the django-admin shell
	docker-compose exec paul ./paul_api/manage.py shell

init-db: superuser                ## sets up the database and fixtures
	docker-compose exec paul ./paul_api/manage.py loaddata statistics
	docker-compose exec paul ./paul_api/manage.py loaddata pages

drop-db:                          ## drops the database
	docker-compose down -t 60
	docker volume rm paul-pgdata

redo-db: drop-db init-db          ## drops the database, then sets up the database and fixtures

## [UTILS]
requirements-build:               ## run pip compile and add requirements from the *.in files
	docker-compose run --rm --no-deps --entrypoint "bash -c" paul "cd /opt && pip-compile -o requirements.txt requirements.in && pip-compile -o requirements-dev.txt requirements-dev.in"

requirements-update:              ## run pip compile and rebuild the requirements files
	docker-compose run --rm --no-deps --entrypoint "bash -c" paul "cd /opt && pip-compile -r -U -o requirements.txt requirements.in && pip-compile -r -U -o requirements-dev.txt requirements-dev.in && chmod a+r requirements.txt && chmod a+r requirements-dev.txt"

migrations:                       ## generate migrations in a clean container
	docker-compose exec paul ./paul_api/manage.py makemigrations

migrate:                          ## apply migrations in a clean container
	docker-compose exec paul ./paul_api/manage.py migrate

makemessages:                     ## generate the strings marked for translation
	docker-compose exec paul ./paul_api/manage.py makemessages -a

compilemessages:                  ## compile the translations
	docker-compose exec paul ./paul_api/manage.py compilemessages

collectstatic:                    ## collect static files (this will take a while)
	docker-compose exec paul ./paul_api/manage.py collectstatic --no-input

black:                            ## run the Black formatter on the Python code
	black --line-length 120 --target-version py39 --exclude migrations ./paul_api

## [TEST]
test:
	docker-compose run --rm paul ./paul_api/manage.py test

#test:                             ## run all tests
#	docker-compose run --rm paul "pytest"
#
#test-pdb:                         ## run tests and enter debugger on failed assert or error
#	docker-compose run --rm paul "pytest --pdb"
#
#test-lf:                          ## rerun tests that failed last time
#	docker-compose run --rm paul "pytest --lf"

## [CLEAN]
clean: clean-docker clean-py      ## remove all build, test, coverage and Python artifacts

clean-docker:                     ## stop docker containers and remove orphaned images and volumes
	docker-compose down -t 60
	docker system prune -f

clean-py:                         ## remove Python test, coverage, file artifacts, and compiled message files
	find ./paul_api -name '.coverage' -delete
	find ./paul_api -name '.pytest_cache' -delete
	find ./paul_api -name '__pycache__' -delete
	find ./paul_api -name 'htmlcov' -delete
	find ./paul_api -name '*.pyc' -delete
	find ./paul_api -name '*.pyo' -delete
	find ./paul_api -name '*.mo' -delete
