#!/usr/bin/python3
"""
Index view for API
"""
from api.v1.views import app_views
from flask import jsonify


@app_views.route('/status', methods=['GET'])
def status():
    """
    Return a JSON response with the status
    """
    return jsonify({"status": "OK"})
