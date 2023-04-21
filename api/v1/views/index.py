#!/usr/bin/env python3
"""
Index view module.
"""
from api.v1.views import app_views
from flask import jsonify


@app_views.route('/status', methods=['GET'])
def status():
    """
    GET /status
    """
    return jsonify({'status': 'OK'})
