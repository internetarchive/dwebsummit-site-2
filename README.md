# Decentralized Web Summit Website

This contains the source for decentralizedweb.net.


# License

AGPL-3


# Development

This is a Django project.


## Python

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

Note, `stdimage` was added to repo, so it could be modified to allow image upscaling. I'd like to fork it and use that later.


If you make changes to the models, you'll need to create migrations and migrate the DB.

```
python ./dwebsummit/manage.py migrate
```

## Directory structure

`/` -- these are root files, not meant to be deployed with the application

`/dwebsummit`  -- this is the application's root

`/dwebsummit/dwebsummit` -- this is the primary django app, which contains settings

`/dwebsummit/dwebsummit_frontend` -- the frontend code (html templates, css, js, etc)

`/dwebsummit/public` -- the server should serve this directory of files


## Frontend

This site used to be implemented using the static-site generator Wintersmith. It was ported to Django in order to add a CMS.

In order to simplify the porting process, some of the same structure was used in Django:
- The frontend templates are written in the Jinja2 language.
- The routes are defined in the admin with the Page.page_url field.


## Hosting


### Dreamhost

This project is structured to work on Dreamhost shared hosting:
- The directory `dwebsummit` contains the Django project.
- Requirements are installed in two directories without using a virtualenv.
  - `sitepackages` is for pure python packages. These are installed locally with `make install`, and included in the `rsync` to the server.
  - `compiledpackages` are for python packages that contain compiled code. Unfortunately, these need to be separately on the server. See *Bootstrapping the server*.
- The package `python-dotenv` is used enable runtime configuration of the application via a `.env` file. See [https://12factor.net/config](https://12factor.net/config).


### Bootstrapping the server

Some modules contain binary code and need to be compiled on the server itself.

This project needs `MySQL-python==1.2.5` for database library and `pillowfight` for image processing.

```
ssh myserver
cd path/to/dwebsummit
make install_compiled
```

Also do this in your local directory.


### Database

A MySQL database is required. You can configure this through the ENV var `DATABASE_URL`. An example value is `mysql://root:@localhost/dwebsummit`. See https://github.com/kennethreitz/dj-database-url.

Run `make migrate` (eg `python dwebsummit/manage.py migrate`) to initialize the database.

To create the first user run `python dwebsummit/manage.py createsuperuser`.

OR just download a copy of the production database to your localhost using a tool like Sequel Pro.


### Uploading

See the private repo with deployment scripts.

Alternatively, here is a template for you:
```
rsync -av --delete --exclude={db.sqlite3,*.pyc,./dwebsummit/public/media/*} ./dwebsummit/ me@myserver.com:sitepath
```



# Credits

Internet Archive

Richard Caceres (@rchrd2)
