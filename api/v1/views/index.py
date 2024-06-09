#!/usr/bin/python3
"""
    the index page
"""
from api.v1.views import app_views
from flask import Response
import json


@app_views.route("/status", strict_slashes=False)
def status_page():
    """
        Returns the app_views status
    """
    # jsonify does not support pretty printing
    json_format = json.dumps({"status": "OK"}, indent=2)
    return Response(json_format, mimetype="application/json")
