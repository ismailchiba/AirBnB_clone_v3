#!/usr/bin/python3
"""Flask application for the AirBnB clone API v1."""
import os
from flask import Flask, jsonify
from models import storage
from api.v1.views import app_views

app = Flask(__name__)
app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown_db(exception):
    """Close storage on teardown."""
    storage.close()


@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors and return a JSON response."""
    return jsonify({"error": "Not found"}), 404


if __name__ == "__main__":
    host = os.environ.getenv("HBNB_API_HOST", "0.0.0.0")
    port = int(os.environ.getenv("HBNB_API_PORT", 5000))
    app.run(host=host, port=port, threaded=True)
