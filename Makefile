install:
	pip install -r ./dwebsummit/requirements.txt -t ./dwebsummit/sitepackages

serve:
	python dwebsummit/manage.py runserver

build:
	# Build the scss files
	sass dwebsummit/dwebsummit_frontend/static/css/main.scss  dwebsummit/dwebsummit_frontend/static/css/main.css
	# Collect all static files into public directory
	python dwebsummit/manage.py collectstatic

migrate:
	# Update the database based on model changes
	# NOTE, you'll need to first run python dwebsummit/manage.py makemigrations 
	python dwebsummit/manage.py migrate
