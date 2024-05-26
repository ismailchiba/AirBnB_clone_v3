#!/usr/bin/python3
"""index.py"""

from api.v1.views import app_views
from flask import jsonify


@app_views.route('/status', methods=['GET'], strict_slashes=False)
def route():
    """Retuns an OK status code in json format"""
    response = jsonify({"status": "OK"})
    response.status_code = 200
    return response
