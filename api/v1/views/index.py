#!/usr/bin/python3
"""
This module contains the endpoint definitions for the AirBnB clone API.
"""

from api.v1.views import app_views
from flask import jsonify


@app_views.route('/status', methods=['GET'], strict_slashes=False)
def api_status():
    """
    Returns the status of the API as a JSON response.
    """
    return jsonify({"status": "OK"})
