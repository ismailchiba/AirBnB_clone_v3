#!/usr/bin/python3
"""Views to handle all place objects"""

from models import storage
from api.v1.views import app_views
from models.base_model import BaseModel
from flask import jsonify, abort, request, make_response
from models.city import City
from models.user import User
from models.place import Place


@app_views.route('/cities/<city_id>/places',
                 methods=['GET'], strict_slashes=False)
def all_places(city_id):
    """Retrieve all places objects related to a city"""
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    plac_list = []
    from plc in city.places:
        place_list.append(plc.to_dict())
    return jsonify(place_list)


@app_views.route('/places/<place_id>')
