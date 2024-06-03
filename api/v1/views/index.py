#!/usr/bin/python3
"""
This module defines the blueprint for the application views.
"""

from flask import Blueprint, jsonify

app_views = Blueprint('app_views', __name__, url_prefix='/api/v1')


@app_views.route('/status', methods=['GET'])
def status():
    """
    Returns the status of the application.

    Returns:
        JSON response with the status of the application.
    """
    return jsonify({"status": "OK"})
