#!/usr/bin/python3
"""A new view for State objects
that handles all default RESTFul API actions"""
from models import storage
from models.state import State
from models.city import City
from api.v1.views import app_views
from flask import jsonify, abort, request


@app_views.route("/states/<state_id>/cities",
                 methods=["GET"], strict_slashes=False)
def cities_states_id(state_id):
    """Retrieve state cities by an ID"""
    obj_state = storage.get(State, state_id)
    if obj_state is None:
        abort(404)
    cities_state = []
    for citie in obj_state.cities:
        cities_state.append(citie.to_dict())
    return jsonify(cities_state)


@app_views.route("/cities/<city_id>", methods=["GET"], strict_slashes=False)
def cities_obj(city_id):
    """Retrieve cities by an ID"""
    city_obj = storage.get(City, city_id)
    if city_obj is None:
        abort(404)
    return jsonify(city_obj.to_dict())


@app_views.route("/cities/<city_id>", methods=["DELETE"], strict_slashes=False)
def cities_delete(city_id):
    """Delete city by an ID"""
    city_obj = storage.get(City, city_id)
    if city_obj is None:
        abort(404)
    storage.delete(city_obj)
    storage.save()
    return jsonify({}), 200


@app_views.route("/states/<state_id>/cities",
                 methods=["POST"], strict_slashes=False)
def city_post(state_id):
    """Create a city inside a state"""
    obj_state = storage.get(State, state_id)
    if obj_state is None:
        abort(404)

    data = request.get_json()

    if data is None:
        return jsonify({"error": "Not a JSON"}), 400
    if "name" not in data:
        return jsonify({"error": "Missing name"}), 400

    new_city = City(**data)
    new_city.state_id = state_id
    new_city.save()

    return jsonify(new_city.to_dict()), 201


@app_views.route("/cities/<city_id>", methods=["PUT"], strict_slashes=False)
def city_put(city_id):
    """Update city by an ID"""
    city_obj = storage.get(City, city_id)
    if city_obj is None:
        abort(404)

    data = request.get_json()
    if data is None:
        return jsonify({"error": "Not a JSON"}), 400

    for key, value in data.items():
        if key not in ["id", "state_id", "created_at", "updated_at"]:
            setattr(city_obj, key, value)
    storage.save()
    return jsonify(city_obj.to_dict()), 200
