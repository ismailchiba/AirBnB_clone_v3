#!/usr/bin/python3

from api.v1.views import app_views
from flask import jsonify
from models import storage
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.user import User
from models.review import Review


app_views.url_map.strict_slashes = False


@app_views.route('/status')
def status():
    """Return a JSON-formatted status response."""
    return jsonify({"status": "OK"})


@app_views.route('/stats')
def count_stats():
    """Return a JSON-formatted stats response."""
    stats = {
        "amenities": storage.count(Amenity),
        "cities": storage.count(City),
        "places": storage.count(Place),
        "reviews": storage.count(Review),
        "states": storage.count(State),
        "users": storage.count(User)
    }


count_stats = {
    key: storage.count(value) for key, value in stats.items()
}
return jsonify(count_stats)
