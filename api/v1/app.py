#!/usr/bin/python3
from os import getenv
from flask import Flask, jsonify, make_response

app = Flask(__name__)

from models import storage
from api.v1.views import app_views

app.register_blueprint(app_views)

@app.teardown_appcontext
def storage_close(exception=None):
    """
    closes the connection at the end of the request
    """
    storage.close()

@app.errorhandler(404)
def not_found(error):
    """"custom not found (404) response"""
    return make_response(jsonify({"error": "Not found"}), 404)

if __name__ == "__main__":
    host = getenv('HBNB_API_HOST') or '0.0.0.0'
    port = getenv('HBNB_API_PORT') or '5000'
    app.run(host=host, port=port, threaded=True)
