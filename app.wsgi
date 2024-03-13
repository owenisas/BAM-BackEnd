import sys
import os

os.environ["DATABASE_URL"] = "127.0.0.1"
os.environ["SERVER_ADDRESS"] = "https://script.owenisas.com/"
os.environ["ABSOLUTE_PATH"] = "/var/www/"

# add your project directory to the sys.path
project_home = '/var/www/marketplace_backend/'
if project_home not in sys.path:
    sys.path = [project_home] + sys.path

# import flask app but need to call it "application" for WSGI to work
from app import app as application  # noqa
