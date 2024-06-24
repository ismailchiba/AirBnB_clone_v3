#!/usr/bin/python3
"""
starts a Flask web application
"""
from api.v1.views import app_views
from flask import Flask, jsonify, make_response
from flask_cors import CORS
from models import storage
import os


app = Flask(__name__)
app.register_blueprint(app_views)
cors = CORS(app, resources={r"/*": {"origins": "0.0.0.0"}})


@app.errorhandler(404)
def page_not_found(error):
    """
    Returns a 'Not Found' error response.
    ---
    responses:
      404:
        description: The requested resource was not found.
    """
    return make_response(jsonify({"error": "Not found"}), 404)


@app.errorhandler(400)
def handle_404(exception):
    """
    handles 400 errros
    """
    code = exception.__str__().split()[0]
    description = exception.description
    message = {"error": description}
    return make_response(jsonify(message), code)


@app.teardown_appcontext
def teardown_db(exception):
    """closes the storage on teardown"""
    storage.close()


def launch():
    """App Launcher"""
    # Retrieve host and port from environment variables
    host = os.getenv("HBNB_API_HOST", "0.0.0.0")
    port = os.getenv("HBNB_API_PORT", "5000")
    app.run(host=host, port=int(port), threaded=True)


if __name__ == "__main__":
    launch()
