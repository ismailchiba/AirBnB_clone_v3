from models import storage
from os import environ
from api.v1.views import app_views
from flask import Flask

app = Flask(__name__)
app.url_map.strict_slashes = False
app.config