#!/usr/bin/python3
""" Module returns the status of API """
from flask import Flask, jsonify
from models import storage
from api.v1.views import app_views
import os

# Flask application instance: app
app = Flask(__name__)

# Register app_views blueprint
app.register_blueprint(app_views)

# the environment variables
host = os.getenv('HBNB_API_HOST', '0.0.0.0')
port = int(os.getenv('HBNB_API_PORT', 5000))
threaded = True


@app.teardown_appcontext
def close_app(error=None):
    """
        This methods calls the close method
        on the storage after each request
    """
    storage.close()


@app.errorhandler(404)
def not_found_error(error):
    """
    Error handler for 404 Not Found errors
    """
    return jsonify({"error": "Not found"}), 404


if __name__ == '__main__':
    """ Main flask app"""
    app.run(host=host, port=port, threaded=threaded)
