#!/usr/bin/python3
"""cities.py"""
from flask import jsonify, abort, request
from api.v1.views import app_views, storage
from models.city import City


@app_views.route("/states/<state_id>/cities", methods=["GET"],
                 strict_slashes=False)
def city_by_state(state_id):
    """Retrieves all City objects from a specific state"""
    city = []
    state = storage.get("State", state_id)

    if not state:
        abort(404)
    for obj in state.cities:
        city.append(obj.to_json())

    return jsonify(city)


@app_views.route("/states/<state_id>/cities", methods=["POST"],
                 strict_slashes=False)
def city_create(state_id):
    """Create a new city in the specified state"""
    data = request.get_json(silent=True)
    if data is None:
        abort(400, 'Not a JSON')

    if not storage.get("State", str(state_id)):
        abort(404)

    if "name" not in data:
        abort(400, 'Missing name')

    data["state_id"] = state_id

    new_city = City(**data)
    new_city.save()
    response = jsonify(new_city.to_json())
    response.status_code = 201

    return response


@app_views.route("/cities/<city_id>",  methods=["GET"],
                 strict_slashes=False)
def city_by_id(city_id):
    """Retrieves a specific City object by ID"""

    city = storage.get("City", str(city_id))
    if not city:
        abort(404)

    return jsonify(city.to_json())


@app_views.route("cities/<city_id>",  methods=["PUT"], strict_slashes=False)
def city_put(city_id):
    """Updates specific City object by ID"""
    data = request.get_json(silent=True)
    if data is None:
        abort(400, 'Not a JSON')
    city = storage.get("City", str(city_id))
    if city is None:
        abort(404)
    for key, val in data.items():
        if key not in ["id", "created_at", "updated_at", "state_id"]:
            setattr(city, key, val)
    city.save()
    return jsonify(city.to_json())


@app_views.route("/cities/<city_id>",  methods=["DELETE"],
                 strict_slashes=False)
def city_delete_by_id(city_id):
    """Deletes City by id"""
    city = storage.get("City", str(city_id))
    if city is None:
        abort(404)

    storage.delete(city)
    storage.save()
    return jsonify({})
