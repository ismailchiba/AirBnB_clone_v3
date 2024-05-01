#!/usr/bin/python3
"""Import required module/lib"""
from . import app_views
from flask import jsonify


@app_views.route('/status')
def get_status():
    return jsonify({"status": "OK"})
