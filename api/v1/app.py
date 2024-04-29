#!/usr/bin/python3
"""
created 29 April 2024
@autor: Edogun peter uyi
"""
from models import storage
from os import getenv
from api.v1.views import app_views
from flask import Flask, jsonify, Blueprint
from app.v1.views import app_views
from flask_cors import CORS


app = Flask(__name__)


CORS(app, origins='0.0.0.0')
app.register_blueprint(app_views)
CORS(app_views)

@app.teardown_appcontext
def close_db_sesion(exception=None):
    """ Call the close method of storage instance """
    storage.close()


@app.errorhandler(404)
def not_found_error(error):
    return jsonify({"error": "Not found"}), 404


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, threaded=True)
