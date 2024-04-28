#!/usr/bin/python3
"""Main module for the API."""
from os import getenv
from flask import Flask
from models import storage
from api.v1.views import app_views

app = Flask(__name__)
app.register_blueprint(app_views)
app.url_map.strict_slashes = False


@app.teardown_appcontext
def teardown(self):
    '''Status of the API'''
    storage.close()

if __name__ == "__main__":
    # host = getenv('HBNB_API_HOST')
    # port = getenv('HBNB_API_PORT')
    app.run(host='0.0.0.0', port='5000', threaded=True)
