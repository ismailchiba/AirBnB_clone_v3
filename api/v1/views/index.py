#!/usr/bin/python3
"""Retrieves the number of objects of each type."""

from flask import jsonify
from api.v1.views import app_views
from models import storage

@app_views.route('/api/v1/stats', methods=['GET'])
def get_stats():
    """Retrieves the number of objects of each type."""
    stats = {}
    object_types = ['Amenity', 'City', 'Place', 'Review', 'State', 'User']  # Replace with actual model names
    for obj_type in object_types:
        count = storage.count(obj_type)
        stats[obj_type] = count
    return jsonify(stats)
