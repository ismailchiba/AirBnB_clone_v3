#!/usr/bin/python3
"""
main file to run all the flask blueprinted apps concurrently
"""

from flask import Flask
from models import storage
from os import getenv
from api.v1.views import app_views

API_HOST = str(getenv('HBNB_API_HOST'))
API_PORT = int(getenv('HBNB_API_PORT'))

app = Flask(__name__)

app.register_blueprint(app_views) #url_prefix='/api/v1')


@app.teardown_appcontext
def close_storage(exception=None):
    """
    If HBNB_TYPE_STORAGE=db closes current session
    If HBNB_TYPE_STORAGE=file reloads file and deserialises JSON objects
    """
    storage.close()


if __name__ == "__main__":
    app.run(API_HOST or '0.0.0.0', API_PORT or 5000, threaded=True, debug=True)
