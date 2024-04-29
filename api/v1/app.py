#!/usr/bin/python3

"""
This module creates a new view for Amenity objects
It handles all default RestFul API actions
And a new route that retrieves the count of all Amenity objects
Create a Flask app that serves the content of the AirBnB clone v3 RESTful API.
"""

from flask_cors import CORS
import os
from models import storage
from api.v1.views import app_views
from flask import Flask, jsonify



app = Flask(__name__)
"""
This will create a Flask app that serves the content of the AirBnB clone v3 RESTful API.
create a blueprint object that handles all views for the application
And a new route that retrieves the count of all Amenity objects
"""

app_host = os.getenv('HBNB_API_HOST', '0.0.0.0')
app_port = int(os.getenv('HBNB_API_PORT', '5000'))
app.url_map.strict_slashes = False
app.register_blueprint(app_views)
CORS(app, resources={'/*': {'origins': app_host}})


@app.teardown_appcontext
def teardown_flask(exception):
    """
    This will remove the current SQLAlchemy Session after each request
    And a new route that retrieves the count of all Amenity objects
    remove the current SQLAlchemy Session after each request
    """
    storage.close()


@app.errorhandler(404)
def error_404(error):
    '''
    This will handle the 404 HTTP error code
    If the error is an instance of Exception and has a description attribute
    Handles the 404 HTTP error code.
    '''
    return jsonify(error='Not found'), 404


@app.errorhandler(400)
def error_400(error):
    '''
    This will handle the 400 HTTP error code
    Handles the 400 HTTP error code.
    And a new route that retrieves the count of all Amenity objects
    '''
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
