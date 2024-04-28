#!/usr/bin/python3
"""
This module contains the principal application
"""
from api.v1.views import app_views
from flask import Flask, jsonify
from models import storage
from os import getenv

app = Flask(__name__)
app.register_blueprint(app_views)


@app.teardown_appcontext
def close_db(obj):
    """
    Close the storage when the application context ends.

    Args:
        exception (Exception): An optional exception
        that occurred during request handling.
    """
    storage.close()


if __name__ == "__main__":

    # Get the host from the environment variable or use default value
    host = getenv('HBNB_API_HOST', default='0.0.0.0')

    # Get the port from the environment variable or use default value
    port = getenv('HBNB_API_PORT', default=5000)

    # Run the Flask app with the specified host, port, and threaded=True
    app.run(host, int(port), threaded=True)
