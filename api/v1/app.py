#!/usr/bin/python3
""" let's configure a flask app
"""

from flask import Flask, jsonify
from models import storage
import os
from api.v1.views import app_views

app = Flask(__name__)
app.register_blueprint(app_views)
app.url_map.strict_slashes = False


@app.teardown_appcontext
def close_store(self):
    '''close the storage'''
    storage.close()


@app.errorhandler(404)
def sorry_page_not_found(error):
    """
    Handles 404 errors by returning a JSON response indicating the error.
    """
    return jsonify({"error": "Not found"}), 404


def get_environment_variable(var_name, default_value):
    """
    Retrieves the value of an environment variable
    or returns a default value if the variable is not set.
    """
    return os.getenv(var_name, default_value)


if __name__ == "__main__":
    host = get_environment_variable('HBNB_API_HOST', '0.0.0.0')
    port = get_environment_variable('HBNB_API_PORT', '5000')
    app.run(host=host, port=port, threaded=True)
