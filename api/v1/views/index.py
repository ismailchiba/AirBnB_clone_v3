#!/usr/bin/python3

"""API routes"""

from api.v1.views import app_views
from flask import jsonify


@app_views.route('/status', methods=['GET'])
def status():
    """Status"""
    return jsonify({"status": "OK"})
