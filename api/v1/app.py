#!/usr/bin/python3

""" This module sets blue print for app"""


from flask import Flask, make_response, jsonify
from models import storage
from api.v1.views import app_views
import os


app = Flask(__name__)
app.register_blueprint(app_views)


@app.teardown_appcontext
def tear_down(error=None):
    """ Tears down or close the db session"""
    storage.close()


@app.errorhandler(404)
def not_found(error):
    """JSON-formatted 404 status code response"""
    error_msg = {"error": "Not found"}
    return make_response(jsonify(error_msg), 404)


if __name__ == "__main__":
    HBNB_API_HOST = os.getenv('HBNB_API_HOST')
    HBNB_API_PORT = os.getenv('HBNB_API_PORT')

    host = HBNB_API_HOST if HBNB_API_HOST else '0.0.0.0'
    port = HBNB_API_PORT if HBNB_API_PORT else '5000'

    app.run(host=host, port=port, threaded=True)
