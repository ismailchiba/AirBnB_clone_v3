#!/usr/bin/python3
"""
Contains route for web status
"""

from flask import jsonify
from api.v1.views import app_views

@app_views.route('/status')
def api_status():
    """
    Returns api status
    """
    response = {'status': "OK"}

    return jsonify(response)