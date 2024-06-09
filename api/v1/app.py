#!/usr/bin/python3
"""
    The API for the AirBnB Clone
"""
from api.v1.views import app_views
from flask import Flask, Response
import json
from models import storage
from os import getenv


app = Flask(__name__)

app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown(exception):
    """
        The teardown function
    """
    storage.close()


@app.errorhandler(404)
def page_not_found(error):
    """
        Handles Resource Not Found
    """
    error_dict = {"error": "Not found"}
    json_format = json.dumps(error_dict, indent=2)
    return Response(json_format, mimetype="application/json", status=404)


if __name__ == "__main__":
    host = getenv("HBNB_API_HOST")
    port = getenv("HBNB_API_PORT")
    if host and port:
        app.run(host=host, port=port, threaded=True)
    else:
        app.run(host="0.0.0.0", port=5000, threaded=True)
