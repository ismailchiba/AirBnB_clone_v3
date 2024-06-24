#!/usr/bin/python3
"""first endpoint APIs"""

import os
from flask import Flask, jsonify
from flask_cors import CORS
from models import storage
from api.v1.views import app_views

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "0.0.0.0"}})
app.register_blueprint(app_views, url_prefix="/api/v1")


@app.teardown_appcontext
def teardown_appcontext(exception):
    """Closes db Sessions"""
    storage.close()


@app.errorhandler(404)
def not_found(error):
    """handle 404 error if found"""
    return jsonify({"error": "Not Found"}), 404


if __name__ == "__main__":
    host = os.getenv("HBNB_API_HOST", "0.0.0.0")
    port = int(os.getenv("HBNB_API_PORT", 5000))
    app.run(host=host, port=port, threaded=True)
