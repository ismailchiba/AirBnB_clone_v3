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


classes = {"Amenity": Amenity, "City": City,
           "Place": Place, "Review": Review, "State": State, "User": User}


@app_views.route('/status', methods=['GET'])
def stat():
    """Returns a JSON"""
    return jsonify({'status': 'OK'})


@app_views.route('/stats', methods=['GET'])
def stats():
    """Retrieves the number of each objects by type"""
    counts = {}
    for cls in classes:
        counts[cls] = storage.count(classes[cls])
    return jsonify(counts)
