#!/usr/bin/python3
"""handles all default RESTFul API actions"""

from flask import jsonify, request, abort
from api.v1.views import app_views
from models import storage
from models.state import City

@app_views.route("/states/<state_id>/cities", methods=["GET"], strict_slashes=False)
def city_all():
    """Retrieves the list of all city  objects """
    city_l = []
    state_o = storage.get("State", state_id)
    if state_o is None:
        abort(404)
    for obj in state_o.values():
        city_l.append(obj.to_dict())

    return jsonify(city_l)

@app_views.route('/cities/<city_id>', methods=['GET'], strict_slashes=False)
def get_city(city_id):
    """Retrieves a city object"""
    ci_ty = storage.get("City", city_id)
    if ci_ty is None:
        abort(404)
    return jsonify(ci_ty.to_dict())                    

@app_views.route("/cities/<city_id>", methods=["DELETE"], strict_slashes=False)
def city_delete(city_id):
    """Deletes a city object"""
    d_obj = storage.get("City", str(city_id))
    if d_obj is None:
        abort(404)

    storage.delete(d_obj)
    storage.save()
    return jsonify({}), 200

@app_views.route("/states/<state_id>/cities", methods=["POST"], strict_slashes=False)
def city_create(state_id):
    """Creates a City"""
    city_j = request.get_json(silent=True)
    
    if not storage.get("State", str(state_id)):
        abort(404)
    if city_j is None:
        abort(400, description='Not a JSON')
    if "name" not in city_j:
        abort(400, description='Missing name')

    city_json["state_id"] = state_id

    new_city = City(**city_j)
    new_city.save()
    repo = jsonify(new_city.to_dict())
    repo.status_code = 201

    return repo

@app_views.route("/cities/<city_id>",  methods=["PUT"], strict_slashes=False)
def city_update(city_id):
    """update a city"""
    city_j = request.get_json(silent=True)
    if city_j is None:
        abort(400, 'Not a JSON')
    d_obj = storage.get("City", str(city_id))
    if d_obj is None:
        abort(404)
    for key, val in city_j.items():
        if key not in ["id", "created_at", "updated_at"]:
            setattr(d_obj, key, val)
    d_obj.save()
    return jsonify(d_obj.to_dict())
