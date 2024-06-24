#!/usr/bin/python3
"""index module"""
from api.v1.views import app_views
from flask import jsonify
from models import storage
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User

@app_views.route('/status', methods=['GET'], strict_slashes=False)
def status():
    """return status"""
    status = {
        "status": "OK"
    }
    response = jsonify(status)
    response.status_code = 200
    return response

@app_views.route('/stats')
def stats():
    """return number of each class"""
    return jsonify({
        "amenities": storage.count(Amenity),
        "cities": storage.count(City),
        "places": storage.count(Place),
        "reviews": storage.count(Review),
        "states": storage.count(State),
        "users": storage.count(User)})
