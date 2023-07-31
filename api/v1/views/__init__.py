#!/usr/bin/python3
""" instances of Blueprint """
from flask import Blueprint
app_views = Blueprint('app_views', __name__, url_prefix="/api/v1")
from api.v1.views.index import *
from api.v1.views.states import *
from api.v1.views.cities import *
from api.v1.views.amenities import *
from api.v1.views.users import *
from api.v1.views.places import *
from api.v1.views.places_reviews import *

def get_status():
    """ returns a JSON """
    return jsonify({"status": "OK"})

def stats():
    clases = {"amenities": Amenity, "cities": City, "places": Place,
              "reviews": Review, "states": State, "users": User}
    my_dict = {}
    for i, j in clases.items():
        my_dict[i] = storage.count(j)
    return jsonify(my_dict)
