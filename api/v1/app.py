#!/usr/bin/python3
"""Module for app file"""

from os import getenv
from flask import Flask, jsonify
from werkzeug.exceptions import NotFound
from api.v1.views import app_views
from models import storage
import os

app = Flask(__name__)

app.register_blueprint(app_views, url_prefix='/api/v1')


@app.errorhandler(404)
def page_not_found(error):
    """A fn that handle 404 errors"""

    return jsonify({"error": "Not found"}), 404


@app.teardown_appcontext
def teardown_appcontext(exception):
    """a fn that close the current SQLAlchemy session"""

    storage.close()


if __name__ == "__main__":
    host = os.getenv('HBNB_API_HOST', '0.0.0.0')
    port = int(os.getenv('HBNB_API_PORT', 5000))
    app.run(host=host, port=port, threaded=True)
