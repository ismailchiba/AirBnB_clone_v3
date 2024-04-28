#!/usr/bin/python3
"""index file where routes to my api are defined"""

from . import app_views
from flask import jsonify


@app_views.route('/status', strict_slashes=False)
def status():
    """returns the status of the api"""
    return jsonify({'status': 'ok'})
