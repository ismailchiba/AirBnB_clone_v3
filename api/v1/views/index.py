#!/usr/bin/python3
"""index"""

from api.v1.views import app_views
from flask import jsonify


@app_views.route('/status', methods=['GET'], strict_slashes=False)
def status():
    """gets status in json format"""
    return jsonify({"status": "OK"})
