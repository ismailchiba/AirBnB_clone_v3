#!/usr/bin/python3xx
import models
from models import storage
from models.base_model import BaseModel
from api.v1.views import app_views
from flask import jsonify


@app_views.route('/api/v1/stats', methods=['GET'])
def get_status():
    """Get the number of each object by it's type"""
    stats = {
            "amenities": storage.count("Amenity"),
            "cities": storage.count("City"),
            "places": storage.count("Place"),
            "reviews": storage.count("Review"),
            "states": storage.count("State"),
            "users": storage.count("User")
    }
    return jsonify(stats)
