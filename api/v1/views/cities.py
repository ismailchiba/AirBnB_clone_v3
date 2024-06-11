#!/usr/bin/python3
"""
Handles city API
"""
from api.v1.views import app_views
from models.city import City
from models import storage
from flask import jsonify, request, abort
from models.state import State

@app_views.route('/states/<state_id>/cities', methods=['GET'],
                 strict_slashes=False)
def all_cities(state_id):
    """GET method for all cities in a specific state"""
    state = storage.get(State, state_id)
    if not state:
        abort(404)

    city_list = [city.to_dict() for city in storage.all(City).values()
                 if city.state_id == state_id]
    return jsonify(city_list)

@app_views.route('/api/v1/cities/<city_id>', methods=['GET'], strict_slashes=False)
def one_city(city_id):
    """Get method for a specific city"""
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    return jsonify(city.to_dict())
