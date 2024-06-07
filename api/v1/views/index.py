#!/usr/bin/python3
"""
Defines route for status used to check api availability
"""

from api.v1.views.__init__ import app_views
from flask import jsonify


@app_views.route("/status", strict_slashes=False)
def check_status():
    """Returns status of api"""
    return jsonify({"status": "OK"})
