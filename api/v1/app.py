#!/usr/bin/python3
"""Main application file for the API"""
from flask import Flask, jsonify
from flask_cors import CORS
from api.v1.views import app_views
from models import storage
import os

app = Flask(__name__)


# Allow all origins for development
CORS(app, resources={r"/*": {"origins": "*"}})


app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown_db(exception):
    """Close storage on teardown"""
    storage.close()


@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors and return a JSON response"""
    return jsonify({"error": "Not found"}), 404


if __name__ == "__main__":
    host = os.getenv('HBNB_API_HOST', '0.0.0.0')
    port = int(os.getenv('HBNB_API_PORT', 5000))
    app.run(host=host, port=port, threaded=True, debug=True)
