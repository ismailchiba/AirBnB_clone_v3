#!/usr/bin/python3
"""
This file creates endpoint to be return status of API.
"""
from flask import Flask, jsonify
from flask_cors import CORS
from models import storage
from os import getenv
from api.v1.views import app_views

app = Flask(__name__)

app.register_blueprint(app_views)
cors = CORS(app, resources={r"/*": {"origins": "0.0.0.0"}})


@app.errorhandler(404)
def resource_not_found(err):
    return jsonify({"error": "Not found"})


@app.teardown_appcontext
def close_sqlalchemy_sessions(exc):
    storage.close()


if __name__ == '__main__':
    host = getenv('HBNB_API_HOST') or '0.0.0.0'
    port = getenv('HBNB_API_PORT') or 5000
    app.run(host=host, port=port, threaded=True, debug=True)
