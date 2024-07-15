#!/usr/bin/python3
"""
Module for Flask application setup & config
"""
from flask import Flask
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from models import storage
from api.v1.views import app_views


app = Flask(__name__)
app.register_blueprint(app_views)

@app.teardown_appcontext
def teardown(exception):
    """ Close storage session """
    storage.close()

if __name__ == "__main__":
    host = os.getenv('HBNB_API_HOST', '0.0.0.0')
    port = int(os.getenv('HBNB_API_PORT', '5000'))
    app.run(host=host, port=port, threaded=True)
