#!/usr/bin/python3

from flask import Flask
from flask import jsonify
from models import storage
from api.v1.views import app_views

app = Flask(__name__)

app.register_blueprint(app_views)

@app.teardown_appcontext
def close_storage():
    """
    Close the storage when the application context ends.

    Args:
        exception (Exception): An optional exception that occurred during request handling.
    """
    storage.close()


if __name__ == "__main__":
    from os import environ

    # Get the host from the environment variable or use default value
    host = environ.get('HBNB_API_HOST', '0.0.0.0')
    # Get the port from the environment variable or use default value
    port = int(environ.get('HBNB_API_PORT', 5000))

    # Run the Flask app with the specified host, port, and threaded=True
    app.run(host=host, port=port, threaded=True)
