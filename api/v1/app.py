#!/usr/bin/python3
'''Contains a Flask web application API.

   Handles API requests and responses, error handling, and application context
   management.
'''
import os
from flask import Flask, jsonify
from flask_cors import CORS

from models import storage
from api.v1.views import app_views


app = Flask(__name__)
'''Configures the Flask application.'''

app_host = os.getenv('HBNB_API_HOST', '0.0.0.0')
app_port = int(os.getenv('HBNB_API_PORT', '5000'))
app.url_map.strict_slashes = False
app.register_blueprint(app_views)
CORS(app, resources={'/*': {'origins': app_host}})


@app.teardown_appcontext
def teardown_flask(exception):
    '''Closes the storage engine connection upon request/app context
    teardown.'''
    """The Flask app request context end event listener."""
    # print(exception)
    storage.close()


@app.errorhandler(404)
def error_404(error):
    '''Handles 404 Not found errors.

    Returns: JSON response with a more informative error message and status
    code 404.
    '''
    return jsonify(error='Not found'), 404


@app.errorhandler(400)
def error_400(error):
    '''Handles 400 Bad Request errors.

    Returns: JSON response with a more informative error message and status
    code 400.
    '''
    msg = 'Bad request'
    if isinstance(error, Exception) and hasattr(error, 'description'):
        msg = error.description
    return jsonify(error=msg), 400


if __name__ == '__main__':
    app_host = os.getenv('HBNB_API_HOST', '0.0.0.0')
    app_port = int(os.getenv('HBNB_API_PORT', '5000'))
    app.run(
        host=app_host,
        port=app_port,
        threaded=True
    )
