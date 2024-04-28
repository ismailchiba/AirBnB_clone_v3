#!/usr/bin/python3
"""
This module contains endpoint(route) status
"""
from api.v1.views import app_views
from flask import Flask, jsonify

"""Create an instance of Blueprint with the URL prefix /api/v1"""

@app_views.route('/status', strict_slashes=False)
def status():
    """
    Returns a JSON response with the status "OK".

    Returns:
        Response: A JSON response with the status "OK".
    """
    response = {"status": "OK"}
    return jsonify(response)
