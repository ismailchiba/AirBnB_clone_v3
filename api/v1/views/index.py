#!/usr/bin/python3
"""
    the index page
"""
from api.v1.views import app_views
from flask import Response
import json
from models import storage
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User


@app_views.route("/status", strict_slashes=False)
def status_page():
    """
        Returns the app_views status
    """
    # jsonify does not support pretty printing
    json_format = json.dumps({"status": "OK"}, indent=2)
    return Response(json_format, mimetype="application/json")


@app_views.route("/stats", strict_slashes=False)
def get_stats():
    all_stats = {"amenities": storage.count(Amenity),
                 "cities": storage.count(City),
                 "places": storage.count(Place),
                 "reviews": storage.count(Review),
                 "states": storage.count(State),
                 "users": storage.count(User)
                 }

    json_format = json.dumps(all_stats, indent=2)
    return Response(json_format, mimetype="application/json")
