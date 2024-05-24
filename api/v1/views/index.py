#!/usr/bin/python3
"""
defines status route for api
"""
from flask import jsonify
from . import app_views
from models.city import City
from models.place import Place
from models.amenity import Amenity
from models.review import Review
from models.user import User
from models.state import State
from models import storage


@app_views.route('/status')
def api_status():
    return jsonify({"status": "OK"})


@app_views.route('/stats')
def models_stats():
    models = {
        "amenities": Amenity,
        "cities": City,
        "places": Place,
        "reviews": Review,
        "states": State,
        "user": User
    }
    stats_dict = {}
    for model in models:
        stats_dict[model] = storage.count(models[model])
    return jsonify(stats_dict)
