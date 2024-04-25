#!/usr/bin/python3
"""Module for the API."""
from api.v1.views import app_views
from flask import Flask, jsonify, make_response
from os import getenv
from models import storage
from flask_cors import CORS


app = Flask(__name__)
app.url_map.strict_slashes = False

app.register_blueprint(app_views)
cors = CORS(app, resources={r"/*": {"origins": "0.0.0.0"}})


@app.errorhandler(404)
def not_found(error):
    """Return a JSON-formatted 404 status code response."""
    return make_response(jsonify({"error": "Not found"}), 404)


@app.teardown_appcontext
def close_storage(exception):
    """Close the storage on teardown."""
    storage.close()


if __name__ == "__main__":
    app.run(host=getenv('HBNB_API_HOST', '0.0.0.0'),
            port=getenv('HBNB_API_PORT', 5000),
            threaded=True)
