#!/usr/bin/python3

"""This module will create a flask app that serves the content of the AirBnB clone v3 RESTful API.
It will be imported in the app.py module
and will be used to create the app object
"""
from flask import Flask, jsonify
from flask_cors import CORS
import os

from models import storage
from api.v1.views import app_views


app = Flask(__name__)
"""This module will
create a blueprint object that handles all views for the application
It will be imported in the app.py module
"""
app_host = os.getenv('HBNB_API_HOST', '0.0.0.0')
app_port = int(os.getenv('HBNB_API_PORT', '5000'))
app.url_map.strict_slashes = False
app.register_blueprint(app_views)
CORS(app, resources={'/*': {'origins': app_host}})


@app.teardown_appcontext
def teardown_flask(exception):
    """This module will
    remove the current SQLAlchemy Session after each request
    It will be called at the end of each request
    """
    storage.close()


@app.errorhandler(404)
def error_404(error):
    """This module will
    return a JSON-formatted 404 status code response
    if a page is not found
    """
    return jsonify(error='Not found'), 404


@app.errorhandler(400)
def error_400(error):
    """This module will
    return a JSON-formatted 400 status code response
    if a bad request is made
    """
    msg = 'Bad request'
    if isinstance(error, Exception) and hasattr(error, 'description'):
        msg = error.description
    return jsonify(error=msg), 400


if __name__ == '__main__':
    app.run(
        host=os.getenv('HBNB_API_HOST', '0.0.0.0'),
        port=int(os.getenv('HBNB_API_PORT', '5000')),
        threaded=True
    )
