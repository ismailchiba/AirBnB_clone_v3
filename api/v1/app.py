#!/usr/bin/python3
"""
This file contains the configuration and setup
for the AirBnB clone API application.
"""

from models import storage
from flask import Flask, jsonify, make_response
from api.v1.views import app_views
import os

app = Flask(__name__)
# Register the blueprint app_views to the Flask instance app
app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown_app_context(exception):
    """
    Closes the storage connection after each request.
    """
    storage.close()


@app.errorhandler(404)
def not_found(error):
    """
    Handler for 404 errors, returns a JSON-formatted 404 response.
    """
    return make_response(jsonify({"error": "Not found"}), 404)


if __name__ == "__main__":
    """
    Runs the Flask application with specified host and port,
    using environment variables if available.
    """
    host = os.getenv('HBNB_API_HOST', '0.0.0.0')
    port = int(os.getenv('HBNB_API_PORT', 5000))
    app.run(host=host, port=port, threaded=True)
