#!/usr/bin/python3
"""module"""
from api.v1.views import app_views


@app_views.route('/status', methods=['GET'])
def status():
    return jsonify({"status": "OK"})
