#!/usr/bin/python3
"""
Create Flask app; app_views
"""
from flask import jsonify
from api.v1.views import app_views


@app_views.route('/sratus')
def api_status():
    """

    """
    response = {'status': "OK"}
    return jasonify(response)
