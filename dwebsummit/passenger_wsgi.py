# This is the entrypoint for the application when deployed to dreamhost

import sys
import os

sys.path.insert(0, os.path.abspath('sitepackages'))
sys.path.insert(0, os.path.abspath('dwebsummit'))

from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())

from dwebsummit import wsgi
application = wsgi.application
