install:
	pip install -r ./dwebsummit/requirements.txt -t ./dwebsummit/sitepackages

install_compiled:
	pip install -r ./dwebsummit/requirements_compiled.txt -t ./dwebsummit/compiledpackages

serve:
	python dwebsummit/manage.py runserver

build-sass:
	# Build the scss files
	sass dwebsummit/dwebsummit_frontend/static/css/main.scss  dwebsummit/dwebsummit_frontend/static/css/main.css

build: build-sass
	# Collect all static files into public directory
	python dwebsummit/manage.py collectstatic

makemigrations:
	python dwebsummit/manage.py makemigrations

migrate:
	# Update the database based on model changes
	# NOTE, you'll need to first run python dwebsummit/manage.py makemigrations
	python dwebsummit/manage.py migrate
