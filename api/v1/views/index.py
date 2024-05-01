#!/usr/bin/python3
"""create flask app; index file"""
from flask import jsonify
from api.v1.views import app_views


@app_views.route('/status', methods=['GET'], strict_slashes=False)
def api_status():
    """Restful API status"""
    return jsonify({"status": "OK"})
