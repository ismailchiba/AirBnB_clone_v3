#!/usr/bin/python3
"""index file"""


from api.v1.views import app_views
from flask import jsonify
from models import storage


@app_views.route('/status', strict_slashes=False)
def status():
    """Simple function that returns status: ok"""
    return jsonify({"status": "OK"})
