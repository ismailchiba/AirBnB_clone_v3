#!/usr/bin/python3
"""Index for Route Module"""

from flask import jsonify
from api.v1.views import app_views
from models import storage
from models.base_model import classes


@app_views.route('/status', methods=['GET'], strict_slashes=False)
def status():
    """Returns the status of the API"""
    return jsonify({"status": "OK"})


@app_views.route('/stats', methods=['GET'], strict_slashes=False)
def get_stats():
    """Returns the number of each object type in the storage"""
    obj_counts = {}
    for cls_name, cls in classes.items():
        obj_counts[cls_name] = storage.count(cls)

    return jsonify(obj_counts)
