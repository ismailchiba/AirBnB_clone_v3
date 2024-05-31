#!/usr/bin/python3
from flask import Flask, Response, jsonify
from models import storage
from api.v1.views import app_views
import os
import json


""" app module - create instance of flask application and handle errors"""


app = Flask(__name__)
app.register_blueprint(app_views)


@app.teardown_appcontext
def tear_down(exception):
    """tear down app session"""

    storage.close()


@app.errorhandler(404)
def error(error):
    """ error handler 404 error """
    error_m = {"error": "Not found"}
    return jsonify(error_m), 404


@app.errorhandler(400)
def bad_request(error):
    """ error handler 404 error """
    error_m = {"error": error.description}
    return jsonify(error_m), 400


if __name__ == "__main__":
    host = os.getenv("HBNB_API_HOST", "0.0.0.0")
    port = int(os.getenv("HBNB_API_PORT", 5000))
    app.run(host=host, port=port, threaded=True)
