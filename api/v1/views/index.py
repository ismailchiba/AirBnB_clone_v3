#!/usr/bin/python3
"""
this is the indedx module
"""

from api.v1.views import app_views
from flask import jsonify

@app_views.route('/status')
def status():
    """returns status : OK"""
    response = {
        'status': 'OK'
    }
    return response
