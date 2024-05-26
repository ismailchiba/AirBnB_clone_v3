#!/usr/bin/python3
"""
AirBnB clone - RESTful API using flask
"""
from os import getenv
from flask import Flask, render_template, request
from models import storage
from api.v1.views import app_views

app = Flask(__name__)

@app.teardown_appcontext
def teardown_appcontext():
    """teardown method"""
    storage.close()

if __name__ == "__main__":
    """run flask server"""
    host = getenv('HBNB_API_HOST', '0.0.0.0')
    port = int(getenv('HBNB_API_PORT', 5000))
    app.run(host=host, port=port, threaded=True)
