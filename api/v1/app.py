#!/usr/bin/python3
"""
This module sets up a Flask web application for the API.

It initializes the Flask app, registers the API blueprint,
and defines error handlers and teardown contexts.
"""

from os import getenv

from flask import Flask, jsonify, make_response
from flask_cors import CORS

from api.v1.views import app_views
from models import storage

app = Flask(__name__)
app.register_blueprint(app_views)

CORS(app, resources={r"/api/v1/*": {"origins": "0.0.0.0"}})


@app.teardown_appcontext
def close_session(exception):
    """
    Close the storage session.

    This function is called after each request to close the
    storage session.
    """
    storage.close()


@app.errorhandler(404)
def not_found(error):
    """
    Return a JSON-formatted 404 status code response.

    This function handles 404 errors by returning a JSON
    response with an error message.

    Args:
        error: The error object (not used in this function).

    Returns:
        response (tuple): A tuple containing the JSON response
        and the 404 status code.
    """
    data = {"error": "Not found"}
    response = jsonify(data), 404
    return make_response(response)


if __name__ == "__main__":
    API_HOST = getenv("HBNB_API_HOST") or "0.0.0.0"
    API_PORT = getenv("HBNB_API_PORT") or 5000
    app.run(host=API_HOST, port=API_PORT, threaded=True)
