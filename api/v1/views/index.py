#!/usr/bin/python3
"""
module index
- app_views router
"""
from api.v1.views import app_views
from flask import jsonify

@app_views.route('/status')
def status():
    return jsonify({"status": "OK"})
