#!/usr/bin/python3
"""Flask backend to serve the AirBnB clone"""

from flask import Flask
from models import storage
from api.vi.views import app_views


app = Flask(__name__)

app.register_blueprint(app_views, url_prefix='/blueprint')

@app.teardown_appcontext
def tear_down(exception):
    """Tear down and close session"""
    storage.close()
