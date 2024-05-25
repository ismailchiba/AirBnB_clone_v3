#!/usr/bin/python3
"""This is an api version 1"""
from flask import Flask, make_response, jsonify
from models import storage
import os
from api.v1.views import app_views


app = Flask(__name__)
app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown(exception):
    """close all storage"""
    storage.close()


@app.errorhandler(404)
def not_found(error):
    """Error Handlers"""
    return make_response(jsonify({"error": "Not found"}), 404)


if __name__ == "__main__":
    app.run(
        host=os.getenv("HBNB_API_HOST") if os.getenv(
            "HBNB_API_HOST") else "0.0.0.0",
        port=os.getenv("HBNB_API_PORT") if os.getenv(
            "HBNB_API_PORT") else "5000",
        threaded=True
    )
