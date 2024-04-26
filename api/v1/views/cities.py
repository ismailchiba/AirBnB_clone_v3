#!/usr/bin/python3
"""
    A module for cities
"""
from api.v1.views import (app_views, City, storage)
from flask import (abort, jsonify, request)


@app_views.route("/states/<state_id>/cities", methods=["GET"],
                 strict_slashes=False)
def state_all_cities(state_id):
    """
    Retrieves all the cities of a given state_id
    """
    state_obj = storage.get("State", state_id)
    if state_obj is None:
        abort(404)
    all_cities = [city.to_json() for city in state.cities]
    return jsonify(all_cities)


@app_views.route("/cities/<city_id>", methods=["GET"], strict_slashes=False)
def one_city(city_id):
    """
    Retrieves one city of a given city_id
    """
    city_obj = storage.get("City", city_id)
    if city_obj is None:
        abort(404)
    return jsonify(city_obj.to_json())


@app_views.route("/cities/<city_id>", methods=["DELETE"], strict_slashes=False)
def delete_one_city(city_id):
    """
    Deletes a state based on the city_id
    """
    city_obj = storage.get("City", city_id)
    if city_obj is None:
        abort(404)
    storage.delete(city_obj)
    return jsonify({})


@app_views.route("/states/<state_id>/cities", methods=["POST"],
                 strict_slashes=False)
def create_one_city(state_id):
    """
    Creates one city tied with the given state_id based on the JSON body
    """
    try:
        res = request.get_json()
    except Exception as e:
        res = None
    if res is None:
        return "Not a JSON", 400
    if 'name' not in res.keys():
        return "Missing name", 400
    state_obj = storage.get("State", state_id)
    if state_obj is None:
        abort(404)
    # creates the dictionary r as kwargs to create a city object
    cty = City(**r)
    cty.state_id = state_id
    cty.save()
    return jsonify(cty.to_json()), 201


@app_views.route("/cities/<city_id>", methods=["PUT"], strict_slashes=False)
def update_one_city(city_id):
    """
    Updates one city tied with the given state_id based on the JSON body
    """
    city_obj = storage.get("City", city_id)
    if city_obj is None:
        abort(404)
    try:
        res = request.get_json()
    except Exception as e:
        res = None
    if res is None:
        return "Not a JSON", 400
    for item in ("id", "created_at", "updated_at", "state_id"):
        res.pop(item, None)
    for key, value in res.items():
        setattr(city_obj, key, value)
    city_obj.save()
    return jsonify(city_obj.to_json()), 200
