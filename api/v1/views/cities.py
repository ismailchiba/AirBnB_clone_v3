#!/usr/bin/python3
""" Added the view for cities"""


from models.state import State
from models.city import City
from flask import jsonify, abort, request
from models import storage
from api.v1.views import app_views


@app_views.route('/states/<state_id>/cities', methods=['GET'],
                 strict_slashes=False)
def read_cities(state_id):
    """ This Retrieves the list of City objects"""

    state_obj = storage.get(State, state_id)

    if not state_obj:
        abort(404)

    # Retrieves city based on state Id
    all_cities = storage.all(City)
    city_list = [city.to_dict() for city in all_cities.values()
                 if city.state_id == state_id]

    return jsonify(city_list)


@app_views.route('/cities/<city_id>', methods=['GET'], strict_slashes=False)
def read_city(city_id):
    """ This get a city object based on the id"""

    city_obj = storage.get(City, city_id)

    if not city_obj:
        abort(404)

    return jsonify(city_obj.to_dict())


@app_views.route('/cities/<city_id>', methods=['DELETE'], strict_slashes=False)
def delete_city(city_id):
    """ This deletes a city object"""

    city_obj = storage.get(City, city_id)

    if not city_obj:
        abort(404)

    # deletes a city
    storage.delete(city_obj)
    storage.save()

    return jsonify({}), 200


@app_views.route('/states/<state_id>/cities', methods=['POST'],
                 strict_slashes=False)
def create_city(state_id):
    """ This creates a city """

    state_obj = storage.get(State, state_id)

    if not state_obj:
        abort(404)

    if not request.get_json():
        abort(400, description="Not a JSON")

    http_to_json = request.get_json()

    if 'name' not in http_to_json:
        abort(400, description="Missing name")

    # Add the state Id into the dictionary if not exist
    http_to_json['state_id'] = state_id

    new_city_obj = City(**http_to_json)

    # save the new object
    new_city_obj.save()

    return jsonify(new_city_obj.to_dict()), 201  # return the new object


@app_views.route('/cities/<city_id>', methods=['PUT'], strict_slashes=False)
def update_city(city_id):
    """ This updates a city object"""
    city_obj = storage.get(City, city_id)

    if not city_obj:
        abort(404)

    if not request.get_json():
        abort(400, description="Not a JSON")

    http_to_json = request.get_json()

    for key, value in http_to_json.items():
        if key not in ['id', 'state_id', 'created_at', 'updated_at']:
            setattr(city_obj, key, value)  # update the object

    storage.save()

    return jsonify(city_obj.to_dict()), 200
