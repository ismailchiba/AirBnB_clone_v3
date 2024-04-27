#!/usr/bin/python3
"""
Let's start Flask app
"""
from flask import Flask
from models import storage
from api.v1.views import app_views
from os import environ


app = Flask(__name__)


@app.teardown_appcontext
def storage_close(error):
    """ This function close the storage """
    storage.close()


if __name__ == "__main__":
    host1 = environ.get('HBNB_API_HOST')
    port1 = environ.get('HBNB_API_PORT')
    if not host1:
        host = '0.0.0.0'
    if not port1:
        port = '5000'
    app.run(host=host1, port=port1, threaded=True)
