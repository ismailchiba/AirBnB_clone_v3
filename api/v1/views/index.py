#!/usr/bin/python3
"""Returns Json"""
from api.v1.views import app_views
from flask import jsonify

@app_views.route('/status')
def status():
    status = {
        "status" : "OK"
    }
    return jsonify(status)