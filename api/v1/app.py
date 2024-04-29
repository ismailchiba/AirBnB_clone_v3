#!/usr/bin/python3

"""
Starts my application
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
def teardown(exception):
    """
    Teardown
    """
    storage.close()


@app.errorhandler(404)
def error_404(exception):
    """
    Handling 404 error
        Return: 404 json
    """

    data = {
        "error": "Not found"
    }

    response = jsonify(data)
    response.status_code = 404

    return (response)


if __name__ == "__main__":
    app.run(getenv("HBNB_API_HOST"), getenv("HBNB_API_PORT"))
