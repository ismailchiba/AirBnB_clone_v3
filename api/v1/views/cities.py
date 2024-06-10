#!/usr/bin/python3
""" objects that handles all default RestFul API actions for cities """
from models.city import City
from models.state import State
from models import storage
from api.v1.views import app_views
from flask import abort, jsonify, make_response, request


@app_views.route("/states/<state_id>/cities", methods=["GET"],
                 strict_slashes=False)
def get_cites(state_id):
    """Retrieves the list of all City objects"""
    state = storage.get(State, state_id)

    if not state:
        abort(404)

    list_city = []
    for value in state.cities:
        list_city.append(value.to_dict())

    return jsonify(list_city)


@app_views.route("/cities/<city_id>", methods=["GET"], strict_slashes=False)
def get_cites_id(cities_id):
    """Retrieves a City by id"""
    city = storage.get(City, cities_id)
    if not city:
        abort(404)

    return jsonify(city.to_dict())


@app_views.route("/cities/<city_id>", methods=["DELETE"], strict_slashes=False)
def delete_city_id(city_id):
    """Deletes a City object by id"""
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    storage.delete(city)
    storage.save()

    return make_response(jsonify({}), 200)


@app_views.route("/states/<state_id>/cities", methods=["POST"],
                 strict_slashes=False)
def create_city(state_id):
    """Creates a City"""
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    if not request.get_json():
        abort(400, description="Not a JSON")

    city = request.get_json()
    instance = City(**city)
    storage.new(instance)
    storage.save()

    return make_response(jsonify(instance.to_dict()), 201)


@app_views.route("/cities/<city_id>", methods=["PUT"], strict_slashes=False)
def update_city(city_id):
    """Updates a City object by id"""
    if not storage.get(City, city_id):
        abort(404)
    if not request.get_json():
        abort(400, description="Not a JSON")

    city = storage.get(City, city_id)
    city_data = request.get_json()
    ignore_keys = ["id", "created_at", "updated_at"]
    for key, value in city_data.items():
        if key not in ignore_keys:
            setattr(city, key, value)
    storage.save()

    return make_response(jsonify(city.to_dict()), 200)
