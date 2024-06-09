#!/usr/bin/python3
"""module to create route"""

from api.v1.views import app_views
from flask import jsonify


@app_views.route('/status')
def status():
    """Returns a status OK"""
    stat = {'status': 'OK'}
    return jsonify(stat)
