#!/usr/bin/python3
""" this area is for description"""

from api.v1.views import app_views
from flask import make_response, jsonify


@app_views.route('/status', methods=['GET'], strict_slashes=False)
def api_resp():
    """ return api response status"""
    return jsonify({"status": "OK"})
