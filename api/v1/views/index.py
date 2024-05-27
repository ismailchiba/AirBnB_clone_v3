#!/usr/bin/python3

from api.v1.views import app_views
from flask import jsonify

@app_views.route('/status', method=['GET'], strict_slashes=False)
def show():
    """ return "status": "OK" """
    return jsonify({"status": "OK"})
