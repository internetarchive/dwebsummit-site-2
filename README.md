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

Make sure you have Mysql installed on your computer. See that step lower in this document.


To install pure-python requirements run:
```
make install
```

Make sure you installed MySQL on your laptop already. See "Install MySQL on Mac" below.
And then install the compiled python requirements, too. 

```
make install_compiled
```

### Configuration

The app is configured with `.env` files. These are git-ignored, because they are instance-specific and contain database passwords. You may need to create one for your local environment. For example:

Create a file named `.env` and add thise.
```
DATABASE_URL=mysql://root:password@localhost/dwebsummit
```

### Misc python
Note this is how the initial project was created:
```
PYTHONPATH=sitepackages ./sitepackages/django/bin/django-admin.py startproject dwebsummit
```

Note, `stdimage` was added to repo, so it could be modified to allow image upscaling. I'd like to fork it and use that later.


### Database migrations

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

### Requirements

You need to install `sass`.

```
npm install -g sass
```


## Hosting


### Dreamhost

This project is structured to work on Dreamhost shared hosting:
- The directory `dwebsummit` contains the Django project.
- Requirements are installed in two directories without using a virtualenv.
  - `sitepackages` is for pure python packages. These are installed locally with `make install`, and included in the `rsync` to the server.
  - `compiledpackages` are for python packages that contain compiled code. Unfortunately, these need to be separately on the server. See *Bootstrapping the server*.
- The package `python-dotenv` is used enable runtime configuration of the application via a `.env` file. See [https://12factor.net/config](https://12factor.net/config).


### Bootstrapping the server

The pure python requirements are copied over from your local install, but you need to compile some packages on the server itself.

This project needs `MySQL-python==1.2.5` for database library and `pillowfight` for image processing.

```
ssh myserver
cd path/to/dwebsummit
pip install -r ./requirements_compiled.txt -t ./compiledpackages
```

Unfortunately, there's one more step. You need to compile this image processing library:

```
cd stdimage/atkinson
./build.sh
```


### Database

A MySQL database is required. You can configure this through the ENV var `DATABASE_URL`. An example value is `mysql://root:@localhost/dwebsummit`. See https://github.com/kennethreitz/dj-database-url.

Run `make migrate` (eg `python dwebsummit/manage.py migrate`) to initialize the database.

To create the first user run `python dwebsummit/manage.py createsuperuser`.

OR just download a copy of the production database to your localhost using a tool like Sequel Pro.

## Install MySQL on Mac

If you don't have mysql installed, you should install it first: https://dev.mysql.com/downloads/mysql/

And then add this to your `.bash_profile` file:

```
export PATH=$PATH:/usr/local/mysql/bin
```

Install this library
```
brew install mysql-connector-c
```

And follow these steps in order to fix python-mysql library installation.
https://stackoverflow.com/a/52655550

### More MySQL tidbits

- If you installed mysql 8 on your mac, make sure you use "legacy" password mode. See this stack overflow article: https://stackoverflow.com/a/49966020

- A great free mysql gui client is [SequelPro](https://sequelpro.com). You can use this to import/export data and create new databases.

- You can connect to the remote database with SequelPro by using the SSH tunnel feature.

- 2019-04-09 - I had trouble importing the database exported from Dreamhost (MySQL 5.6 into my local mac install MySQL 8.0.15). I ended up using the CLI `/usr/local/mysql/bin/mysql -u root -p dwebsummit < dwebcamp_prod_2019-04-09.sql`, but after this, SequelPro could no longer open the database.



### Uploading

If you're Archive staff, see the private repo with deployment scripts.

Alternatively, here is a template for you:
```
rsync -av --delete --exclude={db.sqlite3,*.pyc,./dwebsummit/public/media/*} ./dwebsummit/ me@myserver.com:sitepath
```



# Credits

Internet Archive

Richard Caceres (@rchrd2)
Mindy Seu (@mind_seu)
