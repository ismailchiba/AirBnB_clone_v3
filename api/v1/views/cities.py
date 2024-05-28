#!/usr/bin/python3
"""
Module that handles all default RESTful API actions for Cities class
"""

from api.v1.views import app_views
from flask import abort, jsonify, make_response, request
from models import storage
from models.city import City
from models.state import State


@app_views.route(
    "/states/<state_id>/cities", methods=["GET"], strict_slashes=False
)
def get_cities(state_id):
    """retrieves all City objects"""
    obj_state = storage.get(State, state_id)
    if not obj_state:
        abort(404)
    return jsonify([city.to_dict() for city in obj_state.cities])


@app_views.route("/cities/<city_id>", methods=["GET"], strict_slashes=False)
def get_city(city_id):
    """retrieves a single City object"""
    obj = storage.get(City, city_id)
    if not obj:
        abort(404)
    return jsonify(obj.to_dict())


@app_views.route(
    "/states/<state_id>/cities", methods=["POST"], strict_slashes=False
)
def create_city(state_id):
    """creates a new City object"""
    obj_state = storage.get(State, state_id)
    if not obj_state:
        abort(404)

    new_city = request.get_json()
    if not new_city:
        abort(400, "Not a JSON")
    if "name" not in new_city:
        abort(400, "Missing name")

    obj = City(**new_city)
    setattr(obj, "state_id", state_id)
    storage.new(obj)
    storage.save()
    return make_response(jsonify(obj.to_dict()), 201)


@app_views.route("/cities/<city_id>", methods=["PUT"], strict_slashes=False)
def update_city(city_id):
    """updates a City object"""
    obj = storage.get(City, city_id)
    if not obj:
        abort(404)

    req = request.get_json()
    if not req:
        abort(400, "Not a JSON")

    for key, value in req.items():
        if key not in ["id", "created_at", "update_at", "state_id"]:
            setattr(obj, key, value)

    storage.save()
    return make_response(jsonify(obj.to_dict()), 200)


@app_views.route("/cities/<city_id>", methods=["DELETE"], strict_slashes=False)
def delete_city(city_id):
    """deletes a City object"""
    obj = storage.get(City, city_id)
    if not obj:
        abort(404)
    obj.delete()
    storage.save()
    return make_response(jsonify({}), 200)
