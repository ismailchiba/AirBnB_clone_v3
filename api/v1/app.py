#!/usr/bin/python3

from flask import Flask, jsonify
from flask_cors import CORS
from models import storage
from api.v1.views import app_views
from os import getenv

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "0.0.0.0"}})

app.register_blueprint(app_views, url_prefix="/api/v1")


@app.teardown_appcontext
def teardown(Exception):
    storage.close()


if __name__ == "__main__":

    host = getenv("HBNB_API_HOST")
    port = getenv("HBNB_API_PORT")
    app.run(host=host, port=port, threaded=True)
