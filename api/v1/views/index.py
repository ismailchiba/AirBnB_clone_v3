#!/usr/bin/python3
"""
Cresate flask app
"""
from flask import jsonify
from api.v1.views import app_views

@app_views.route('/status')
def api_status():
    """
    Api status
    """
    response = {'status': "OK"}
    return jsonify(response)
