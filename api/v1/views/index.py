#!/usr/bin/python3
"""
    index module
"""
from flask import jsonify
from api.v1.views import app_views
from models import storage
from models.state import State
from models.amenity import Amenity
from models.place import Place
from models.review import Review
from models.city import City
from models.user import User


@app_views.route("/status", methods=['GET'], strict_slashes=False)
def status():
    """send a 200 reponse to cliet with format 'status': 'ok'"""
    return jsonify(status="OK")

@app_views.route("/stats", methods=['GET'], strict_slashes=False)
def stats():
    """return the current count in the db"""
    stat = {
            'amentities': storage.count(Amenity),
            'cities': storage.count(City),
            'places': storage.count(Place),
            'reviews': storage.count(Review),
            'states': storage.count(State),
            'users': storage.count(User),
           }
    return jsonify(stat)
