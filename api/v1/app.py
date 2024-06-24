#!/usr/bin/python3
"""sets up the Flask application for v1 of the API"""

from api.v1.views import app_views
from flask import Flask, jsonify
from models import storage
import os


app = Flask(__name__)
app.register_blueprint(app_views)


@app.teardown_appcontext
def close_session(exception=None):
    storage.close()


@app.errorhandler(404)
def not_found(error):
    response = jsonify({"error": "Not found"})
    response.status_code = 404
    return response


if __name__ == "__main__":
    host = os.getenv("HBNB_API_HOST", "0.0.0.0")
    port = int(os.getenv("HBNB_API_PORT", "5000"))
    app.run(host=host, port=port, threaded=True)
