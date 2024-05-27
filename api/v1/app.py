#!/usr/bin/python3
"""
Main Flask application setup.
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
    Teardown function to close storage connection.
    """
    storage.close()


@app.errorhandler(404)
def handle_404(exception):
    """
    Custom error handler for 404 Not Found errors.
    """
    data = {
        "error": "Not found"
    }
    return jsonify(data), 404


if __name__ == "__main__":
    app.run(host=getenv("HBNB_API_HOST", "0.0.0.0"),
            port=getenv("HBNB_API_PORT", 5000),
            threaded=True)
