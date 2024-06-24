#!/usr/bin/python3
"""Start your API"""
from flask import Flask, jsonify
from models import storage
from api.v1.views import app_views
from flask_cors import CORS
import os


app = Flask(__name__)
cors = CORS(app, resources={r"/api/*": {"origins": "0.0.0.0"}})
app.register_blueprint(app_views)


@app.teardown_appcontext
def close(exception):
    """Close storage"""
    storage.close()


@app.errorhandler(404)
def not_found(exception):
    """A handler for 404 errors"""
    return jsonify({"error": "Not found"}), 404


if __name__ == "__main__":
    """Set environment variable for host and port"""
    # Set host with HBNB_API_HOST env var or '0.0.0.0' if not defined
    host = os.environ.get("HBNB_API_HOST", "0.0.0.0")
    # Set port with HBNB_API_PORT env var or 5000 if not defined
    port = int(os.environ.get("HBNB_API_PORT", 5000))
    # Run the Flask server with the specified parameters
    app.run(host=host, port=port, threaded=True)
