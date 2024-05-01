#!/usr/bin/python3
"""
designig a flask app by importing the necessities
"""

from flask import Flask, jsonify
from flask_cors import CORS
from models import storage
from api.v1.views import app_views
from os import getenv

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "0.0.0.0"}})

app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown(Exception):
    storage.close()


@app.errorhandler(404)
def detect_issue(error):
    response = show_response(jsonify({'error': 'Not found'}), 404)
    return response


if __name__ == "__main__":
    host = getenv("HBNB_API_HOST", "0.0.0.0")
    port = getenv("HBNB_API_PORT", 5000)
    app.run(host=host, port=port, threaded=True)
