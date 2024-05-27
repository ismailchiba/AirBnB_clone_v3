#!/usr/bin/python3
"""This is an api version 1"""
from flask import Flask, make_response, jsonify
from models import storage
import os
from api.v1.views import app_views
from flask_cors import CORS


app = Flask(__name__)
app.register_blueprint(app_views)

cors = CORS(app, resources={r"/api/*": {"origins": "0.0.0.0"}})

@app.teardown_appcontext
def teardown(exception):
    """close all storage"""
    storage.close()


@app.errorhandler(404)
def not_found(error):
    """Error Handlers"""
    return make_response(jsonify({"error": "Not found"}), 404)


if __name__ == '__main__':
    if getenv("HBNB_API_HOST") is None:
        HBNB_API_HOST = '0.0.0.0'
    else:
        HBNB_API_HOST = getenv("HBNB_API_HOST")
    if getenv("HBNB_API_PORT") is None:
        HBNB_API_PORT = 5000
    else:
        HBNB_API_PORT = int(getenv("HBNB_API_PORT"))
    app.run(host=HBNB_API_HOST, port=HBNB_API_PORT, threaded=True)
