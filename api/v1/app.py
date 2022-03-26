#!/usr/bin/python3

"""
Module to check the status of the API
"""

from models import storage
from api.v1.views import app_views
from flask import Flask
app = flask(__name__)

app.register=blueprint(app_views)
@app.teardown_appcontext
def teardown(exception):
    storage.close()

if __name__ == __main__:
    app.run(host = '0.0.0.0', port = '5000')
