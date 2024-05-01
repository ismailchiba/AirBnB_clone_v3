#!/usr/bin/python3
"""Import required module/lib"""
from . import app_views
from flask import jsonify
from models import storage


@app_views.route('/status')
def get_status():
    return jsonify({"status": "OK"})


@app_views.route('/stats')
def stats():
    """retrieves the number of each objects by type"""
    stats = {}
    for cls in storage.classes():
        stats[cls.__name__] = storage.count(cls)

    return jsonify(stats)
