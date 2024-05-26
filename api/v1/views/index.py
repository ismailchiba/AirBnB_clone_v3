#!/usr/bin/python3
"""
API version 1 views
"""
from api.v1.views import app_views
from flask import jsonify


@app_views.route('/status')
def get_status():
    """send status of the server as JSON"""
    return jsonify({"status": "OK"})
