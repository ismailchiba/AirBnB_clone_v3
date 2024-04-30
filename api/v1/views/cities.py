#!/usr/bin/python3
"""handle cities operations"""

from flask import jsonify, abort, request
from api.v1.views import app_views, storage
from models.city import City


@app_views.route("/states/<state_id>/cities", methods=["GET"], strict_slashes=False)
def get_city_by_state(state_id):
    """retrieves the list of all City from a state"""
    city_list = []
    state_obj = storage.get("State", state_id)

    if state_obj is None:
        abort(404)
    for obj in state_obj.cities:
        city_list.append(obj.to_json())
    return jsonify(city_list)



@app_views.route("/cities/<city_id>",  methods=["GET"],
                 strict_slashes=False)
def get_city_id(city_id):
    """gets a city by its ID"""
    city_obj = storage.get("City", str(city_id))
    if city_obj is None:
        abort(404)
    return jsonify(city_obj.to_json())


@app_views.route("/states/<state_id>/cities", methods=["POST"], strict_slashes=False)
def city_create(state_id):
    """create a city"""
    city_json = request.get_json(silent=True)
    if city_json is None:
        abort(400, 'Not a JSON')
    if not storage.get("State", str(state_id)):
        abort(404)
    if "name" not in city_json:
        abort(400, 'Missing name')

    city_json["state_id"] = state_id
    new_city = City(**city_json)
    new_city.save()
    resp = jsonify(new_city.to_json())
    resp.status_code = 201

    return resp


@app_views.route("cities/<city_id>",  methods=["PUT"], strict_slashes=False)
def put_city(city_id):
    """updates City object by its id"""
    city_json = request.get_json(silent=True)
    if city_json is None:
        abort(400, 'Not a JSON')
    city_obj = storage.get("City", str(city_id))
    if city_obj is None:
        abort(404)
    for key, value in city_json.items():
        if key not in ["id", "created_at", "updated_at", "state_id"]:
            setattr(city_obj, key, value)
    city_obj.save()
    return jsonify(city_obj.to_json())


@app_views.route("/cities/<city_id>",  methods=["DELETE"], strict_slashes=False)
def city_delete(city_id):
    """deletes City by the use of its id"""
    city_obj = storage.get("City", str(city_id))

    if city_obj is None:
        abort(404)
    storage.delete(city_obj)
    storage.save()

    return jsonify({})
