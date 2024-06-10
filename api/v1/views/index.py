#!/usr/bin/python3
"""
flask app
"""
from flask import jsonify
from api.v1.views import app_views


@app_views.route('/status', methods=['GET'])
def api_status():
    """
    status route
    """
    response = {"status": "OK"}
    return jsonify(response)
