ifneq (,$(wildcard ./.env))
include .env
export 
ENV_FILE_PARAM = --env-file .env

endif

create_env:
	python3.12 -m venv venv

# act:  # doesn't work
# 	source venv/bin/activate
# realpath venv

mmig: 
	python manage.py makemigrations

mig: 
	python manage.py migrate

serv:
	python manage.py runserver

serv-plus:
	python manage.py runserver_plus --cert-file cert.crt
	
suser:
	python manage.py createsuperuser

cpass:
	python manage.py changepassword

shell:
	python manage.py shell

sapp:
	python manage.py startapp

reqn:
	pip install -r requirements.txt

ureqn:
	pip freeze > requirements.txt

help:  ## makefile documentation.
	@sed -ne '/@sed/!s/## //p' $(MAKEFILE_LIST)

lint: ## lint & format
	pre-commit run --all-files

init_db: ## init db
	python manage.py initd

# DOCKER COMMANDS
build:
	docker-compose up --build -d --remove-orphans

up:
	docker-compose up -d

down:
	docker-compose down

show-logs:
	docker-compose logs

redis:
	sudo docker run -it --rm --name redis -p 6378:6379 redis

celery:
	celery -A tech_hive worker -l info --pool=solo

ngrok:
	ngrok http 9000

psql:
	sudo -u postgres psql

dbshell:
	python manage.py dbshell

cpp:
	python manage.py create_premium_plan

clean-media: 
	python manage.py deleteorphanedmedia --noinput=False

clean-static: 
	python manage.py deleteredundantstatic

clean-cloudinary: 
	python manage.py deleteorphanedmedia
	python manage.py deleteredundantstatic

tests:
	python manage.py test

check:
	python manage.py check

check-deploy:
	python manage.py check --deploy 

export_emails:
	python manage.py export_emails > emails.txt

secret-key:
	python manage.py generate_secret_key

show-permissions:
	python manage.py show_permissions

update-permissions:
	python manage.py update_permissions

clear-cache:
	python manage.py clear_cache

notes:
	python manage.py notes

flush-tokens: 
    python manage.py flushexpiredtokens

flush-tokens-verbose:
	python manage.py cleanup_tokens_verbose

# python manage.py loaddata fixtures/content.json -v 2
# ngrok http https://127.0.0.1:8000
# base64 .env > .env.base64