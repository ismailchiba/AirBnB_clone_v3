#!/usr/bin/python3
"""HBNB API Flask application"""

from flask import Flask, make_response, jsonify
from models import storage  # Assuming models.py defines storage engine
from api.v1.views import app_views
from os import getenv
from flask_cors import CORS
import logging

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['LOGLEVEL'] = logging.INFO

cors = CORS(app, resources={r"/api/*": {"origins": "0.0.0.0"}})

app.url_map.strict_slashes = False
app.register_blueprint(app_views)


@app.teardown_appcontext
def tear(self):
    """Closes storage engine"""
    storage.close()


@app.errorhandler(404)
def not_found(error):
    """Handles 404 error and gives JSON formatted response"""
    return make_response(jsonify({'error': 'Not found'}), 404)


@app.errorhandler(500)
def internal_server_error(error):
    """Handles 500 error and gives JSON formatted response"""
    # Log the error for debugging
    app.logger.error(f"An internal server error occurred: {error}")
    return make_response(jsonify({'error': 'Internal server error'}), 500)


if __name__ == '__main__':
    logging.basicConfig(filename='hbnb_api.log', level=app.config['LOGLEVEL'])  # Configure logging

    HBNB_API_HOST = getenv("HBNB_API_HOST", '0.0.0.0')
    HBNB_API_PORT = int(getenv("HBNB_API_PORT", 5000))

    app.run(host=HBNB_API_HOST, port=HBNB_API_PORT, threaded=True)
