#!/usr/bin/python3
""" Start a Flask web application """
from os import getenv
from flask import Flask, jsonify
from models import storage
from api.v1.views import app_views
from os import environ


app = Flask(__name__)
app.url_map.strict_slashes = False
app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown_db(exception):
    """ Closes the storage session """
    storage.close()


@app.errorhandler(404)
def page_not_found(e):
    """ Handles the 404 error """
    return jsonify({"error": "Not found!"}), 404


if __name__ == "__main__":
    host = environ.get("HBNB_API_HOST", "0.0.0.0")
    port = environ.get("HBNB_API_PORT", "5000")
    app.run(host=HOST, port=PORT, threaded=True)
    