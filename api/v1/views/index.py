#!/usr/bin/python3
"""
    import app_views from api.v1.views
        create a route /status on the object app_views that returns a JSON: "status": "OK" (see example)
    """
from flask import jsonify
from app.v1.views import app_views

@app_views.route('/status', methods=['GET'])
def get_status():
    route_response = {"status": "OK"}
    return jsonify(route_response)
