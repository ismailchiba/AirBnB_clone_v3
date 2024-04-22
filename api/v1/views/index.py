#!/usr/bin/python3
from flask import jsonify
from api.v1.views import app_views
from models import storage

@app_views.route('/status', methods=['GET'], strict_slashes=False)
def api_status():
    return (jsonify({"status": "OK"}))

@app_views.route('/api/v1/stats', methods=['GET'], strict_slashes=False)
def object_count():
    classes = ['Amenity', 'City', 'Place', 'Review', 'State', 'User']
    key_names = ["amenities", "cities", "places", "reviews", "states", "users"]
    data = {}
    index = 0
    for type in classes:
        count = storage.count(type)
        data[key_names[index]] = count
        index += 1
    return (jsonify(data))
