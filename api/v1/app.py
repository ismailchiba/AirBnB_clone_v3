#!/usr/bin/python3
"""
This script is the entry point for the application.
It initializes the Flask app and registers the blueprints for API endpoints.
"""

from flask import Flask, jsonify
from flask_cors import CORS
from os import getenv

from api.v1.views import app_views
from models import storage


app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "0.0.0.0"}})

app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown_appcontext(exception):
    """
    This function is called when the Flask app context is torn down.
    It is used to close the storage connection.

    :param exception: Exception that caused the teardown.
    """
    storage.close()


@app.errorhandler(404)
def handle_404(exception):
    """
    Handles 404 error.

    :return: Returns 404 JSON.
    """
    data = {
        "error": "Not found"
    }

    resp = jsonify(data)
    resp.status_code = 404

    return resp


if __name__ == "__main__":
    app.run(host=getenv("HBNB_API_HOST"),
            port=getenv("HBNB_API_PORT"))
