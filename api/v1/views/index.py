#!/usr/bin/python3
"""The index of the api"""

from flask import jsonify
from api.v1.views import app_views


@app_views.route('/status')
def get_status():
    """Returns status as OK"""
    return jsonify(status='OK')
