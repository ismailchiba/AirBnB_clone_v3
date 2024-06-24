#!/usr/bin/python3
"""cities module"""

from flask import jsonify, abort, request
from api.v1.views import app_views, storage
from models.city import City
from models.state import State


@app_views.route('/states/<state_id>/cities', methods=['GET'],
                 strict_slashes=False)
def get_city_by_state(state_id):
    """get cities"""
    cities = []
    state_objects = storage.get("State", state_id)
    if state_objects is None:
        abort(404)
    for city in state_objects.cities:
        if city.state_id == state_id:
            cities.append(city.to_dict())
    return jsonify(cities)


@app_views.route('/states/<state_id>/cities', methods=['POST'],
                 strict_slashes=False)
def post_city(state_id):
    """post city"""
    new_city = request.get_json(silent=True)
    if new_city is None:  # check if json post request is valid
        abort(404, "Not a JSON")
    if not storage.get("State", str(state_id)):  # check if state_id exists
        abort(404)
    if 'name' not in new_city:
        abort(400, 'Missing name')
    city = City(**new_city)
    setattr(city, 'state_id', state_id)
    city.save()
    return jsonify(city.to_dict()), 201


@app_views.route("/cities/<city_id>", methods=["GET"], strict_slashes=False)
def get_city_by_id(city_id):
    """get city by id"""
    city_object = storage.get("City", str(city_id))
    if city_object is None:
        abort(404)
    return jsonify(city_object.to_dict())


@app_views.route("cities/<city_id>",  methods=["PUT"], strict_slashes=False)
def put_city(city_id):
    """put city by id """
    city_update = request.get_json(silent=True)
    if city_update is None:
        abort(400, 'Not a JSON')
    city_object = storage.get("City", str(city_id))
    if city_object is None:
        abort(404)
    for key, val in city_update.items():
        if key not in ["id", "created_at", "updated_at", "state_id"]:
            setattr(city_object, key, val)
    city_object.save()
    return jsonify(city_object.to_dict())


@app_views.route("/cities/<city_id>",  methods=["DELETE"],
                 strict_slashes=False)
def city_delete_by_id(city_id):
    """delete city by id"""
    city_object = storage.get("City", str(city_id))
    if city_object is None:
        abort(404)
    storage.delete(city_object)
    storage.save()
    return jsonify({})
