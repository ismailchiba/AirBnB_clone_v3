#!/usr/bin/python3
<<<<<<< HEAD
"""Module contains a flask server."""

from flask import Flask, jsonify
from models import storage
from os import getenv
from api.v1.views import app_views

app = Flask(__name__)
app.register_blueprint(app_views)
app.url_map.strict_slashes = False


@app.teardown_appcontext
def downtear(self):
    """A teardown method"""
=======
"""
API for AirBnB_clone_v3
"""

import os
from flask import Flask, jsonify, Response
from flask_cors import CORS
from models import storage
from api.v1.views import app_views
app = Flask(__name__)
app.register_blueprint(app_views)
cors = CORS(app, resources={r"/*": {"origins": "0.0.0.0"}})


@app.teardown_appcontext
def teardown(self):
    """ handles teardown """
>>>>>>> dff4a60a4ac807bc9108c52bf6cb81f811eec8a5
    storage.close()


@app.errorhandler(404)
<<<<<<< HEAD
def page_not_found(error):
    """It handles errors."""
    return jsonify("error": "Not found"), 404

if __name__ == "__main__":
    host = getenv("HBNB_API_HOST")
    port = getenv("HBNB_API_PORT")
    if not host:
        host = "0.0.0.0"
    if not port:
        port = "5000"
    app.run(host=host, port=port, threaded=True)
=======
def page_not_found(e):
    """ handles 404 errors """
    status = {"error": "Not found"}
    return jsonify(status), 404


if __name__ == '__main__':
    try:
        host = os.environ.get('HBNB_API_HOST')
    except:
        host = '0.0.0.0'

    try:
        port = os.environ.get('HBNB_API_PORT')
    except:
        port = '5000'

    app.run(host=host, port=port)
>>>>>>> dff4a60a4ac807bc9108c52bf6cb81f811eec8a5
