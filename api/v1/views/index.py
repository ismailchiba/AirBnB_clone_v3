#!/usr/bin/python3
"""
This module contains endpoint(route) status
"""
from api.v1.views import app_views
from flask import Flask, jsonify


@app_views.route('/status', strict_slashes=False)
def status():
    """
    Returns a JSON response with the status "OK".

    Returns:
        Response: A JSON response with the status "OK".
    """
    return jsonify(status="OK")
