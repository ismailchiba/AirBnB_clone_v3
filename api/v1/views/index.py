#!/usr/bin/python3
"""creates routes"""


from api.v1.views import app_views
from flask import jsonify
from models import storage
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User


classes = {
    "amenities": Amenity,
    "cities": City,
    "places": Place,
    "reviews": Review,
    "states": State,
    "users": User
}


@app_views.route('/status', methods=['GET'])
def stat():
    """Returns a JSON"""
    return jsonify({'status': 'OK'})


@app_views.route('/stats', methods=['GET'])
def count():
    """Retrieves the number of each objects by type"""
    counts = {}
    for cls in classes:
        counts[cls] = storage.count(classes[cls])
    return jsonify(counts)
