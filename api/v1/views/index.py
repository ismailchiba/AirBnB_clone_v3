#!/usr/bin/python3
"""index.py"""

from api.v1.views import app_views
from flask import jsonify


@app_views.route('/status', strict_slashes=False)
def route():
    """Retuns an OK status code in json format"""
    return jsonify({"status": "OK"})
