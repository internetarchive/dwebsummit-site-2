install:
	pip install -r ./dwebsummit/requirements.txt -t ./dwebsummit/sitepackages

make serve:
	python dwebsummit/manage.py runserver
