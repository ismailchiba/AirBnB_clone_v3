#!/usr/bin/python3
"""
"""
from api.v1.views import app_views
from flask import jsonify

@my_blueprint.route('/status')
def status:
    return jsonify({"status": "OK"})
