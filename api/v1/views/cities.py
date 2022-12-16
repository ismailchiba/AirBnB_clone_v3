#!/usr/bin/python3
"""module is document"""
from api.v1.views import app_views
from flask import jsonify, request, make_response, abort
from models import storage
from models.state import State
#from models.city import City


@app_views.route('/states/<state_id>/cities', methods=['GET'])
def list_cities(state_id):
    if not state_id:
        abort(400)
    all_cities = storage.all(City)
    all_cities = list(v.to_dict() for v in all_cities.values())
    return jsonify(all_cities)


@app_views.route('/cities/<city_id>', methods=['GET'])
def city_obj(city_id):
    city_obj = storage.get(City, city_id)
    if city_obj is None:
        abort(404)
    return jsonify(city_obj.to_dict()), 200


@app_views.route('/cities/<city_id>', methods=['DELETE'])
def delete_city_obj(city_id):
    city_obj = storage.get(City, city_id)
    if city_obj is None:
        abort(404)
    storage.delete(city_obj)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/states/<state_id>/cities', methods=['POST'], strict_slashes=False)
def creates_state(state_id):
    if not state_id:
        abort(404)
    req_json = request.get_json()
    if not request.get_json():
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    if "name" not in request.get_json():
        return make_response(jsonify({"error": "Missing name"}), 400)
    newCity = City()
    for k, v in req_json.items():
        setattr(newCity, k, v)
    storage.new(newCity)
    storage.save()
    return make_response(jsonify(newCity.to_dict()), 201)


@app_views.route('/cities/<city_id>', methods=['PUT'], strict_slashes=False)
def update_state(city_id):
    if not city_id:
        abort(404)
    obj = storage.get(City, city_id)
    if not obj:
        return make_response(jsonify({"error": "Not found"}), 404)
    json_obj = request.get_json()
    if not json_obj:
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    for k, v in json_obj.items():
        if k not in ["id", "created_at", "updated_at"]:
            setattr(obj, k, v)
    obj.save()
    return make_response(jsonify(obj.to_dict()), 200)
