## Development setup

### Python

This is a python27 project

Since this uses local requirements, you need to modify a file called `~/.pydistutils.cfg` with the following content.

```
[install]
prefix=
```

To install requirements run:
```
make install
```


Note this is how the initial project was created:
```
PYTHONPATH=sitepackages ./sitepackages/django/bin/django-admin.py startproject dwebsummit
```

If you make changes to the models, you'll need to create migrations and migrate the DB.

```
python ./dwebsummit/manage.py migrate
```

### Directory structure

`/` -- these are root files, not meant to be deployed with the application

`/dwebsummit`  -- this is the application's root

`/dwebsummit/dwebsummit` -- this is the primary django app, which contains settings

`/dwebsummit/dwebsummit_frontend` -- the frontend code (html templates, css, js, etc)

`/dwebsummit/public` -- the server should serve this directory of files


### Frontend

The frontend templates are written in the Jinja2 language.


## Deployment

See the private repo with deployment scripts.

Alternatively, here is a template for you:
```
rsync -av --delete --exclude={db.sqlite3,*.pyc,./dwebsummit/public/media/*} ./dwebsummit/ me@myserver.com:sitepath
```


### Bootstrapping the server

Some modules contain binary code and need to be compiled on the server itself.

```
ssh myserver
cd path/to/dwebsummit
pip install -t compiledpackages MySQL-python==1.2.5 pillowfight==0.3
```

Also do this in your local directory.



## Credits

Internet Archive

Richard Caceres (@rchrd2)
