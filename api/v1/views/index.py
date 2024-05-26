#!/usr/bin/python3
"""
API version 1 views
"""
from api.v1.views import app_views
from flask import jsonify
from models import storage


@app_views.route('/status')
def get_status():
    """send status of the server as JSON"""
    return jsonify({"status": "OK"})


@app_views.route('/stats')
def get_stats():
    """send the number of each objects by type:
    """
    from models.engine.file_storage import classes
    tmp = {key.lower(): storage.count(value) for key, value in classes.items()}
    return jsonify(tmp)
