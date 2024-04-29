#!/usr/bin/python3

'''
This is the main module for the API called app.py
It does the following:
- creates a Flask instance
- creates a blueprint object that handles all views for the application
- registers the blueprint app_views
- handles the 404 HTTP error code
- handles the 400 HTTP error code
- runs the application
'''
from flask import Flask, jsonify
from flask_cors import CORS
import os

from models import storage
from api.v1.views import app_views


app = Flask(__name__)
"""
This is the main module for the API called app.py
It does the following:
create a blueprint object that handles all views for the application
"""
app_host = os.getenv('HBNB_API_HOST', '0.0.0.0')
app_port = int(os.getenv('HBNB_API_PORT', '5000'))
app.url_map.strict_slashes = False
app.register_blueprint(app_views)
CORS(app, resources={'/*': {'origins': app_host}})


@app.teardown_appcontext
def teardown_flask(exception):
    """
    This function will
    remove the current SQLAlchemy Session after each request
    It will close the storage
    """
    storage.close()


@app.errorhandler(404)
def error_404(error):
    '''
    This is where the 404 error is handled
    Handles the 404 HTTP error code.
    '''
    return jsonify(error='Not found'), 404


@app.errorhandler(400)
def error_400(error):
    '''
    This is where the 400 error is handled
    It is a bad request
    Handles the 400 HTTP error code.'''
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
