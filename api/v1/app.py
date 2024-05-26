#!/usr/bin/python3
"""create variable"""
from api.v1.views import app_views
from flask import Flask, Blueprint
from models import storage
from os import getenv

app = Flask(__name__)

app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown_app(obj):
    """registers a function when app contect is torn down"""
    storage.close()


if __name__ == "__main__":
    host = getenv('HBNB_API_HOST', default='0.0.0.0')
    port = getenv('HBNB_API_PORT', default=5000)
    app.run(host, int(port), threaded=True)
