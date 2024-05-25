#!/usr/bin/python3
""" handles all default RESTFul API actions"""

from flask import jsonify, request, abort
from api.v1.views import app_views
from models import storage
from models.place import Place

@app_views.route("/places", methods=["GET"], strict_slashes=False)
def place_all():
    """Retrieves the list of all Place objects """
    place_l = []
    place_o = storage.all("Place")
    for obj in place_o.values():
        place_l.append(obj.to_dict())

    return jsonify(place_l)

@app_views.route('/places/<place_id>', methods=['GET'], strict_slashes=False)
def get_place(place_id):
    """Retrieves a Place object"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    return jsonify(place.to_dict())

@app_views.route("/places/<place_id>", methods=["DELETE"], strict_slashes=False)
def place_delete(place_id):
    """Deletes a Place object"""
    d_obj = storage.get("Place", str(place_id))
    if d_obj is None:
        abort(404)

    storage.delete(d_obj)
    storage.save()
    return jsonify({}), 200

@app_views.route("/places", methods=["POST"], strict_slashes=False)
def place_create():
    """Creates a Place"""
    place_j = request.get_json(silent=True)
    if place_j is None:
        abort(400, description='Not a JSON')
    if "name" not in place_j:
        abort(400, description='Missing name')

    new_place = Place(**place_j)
    new_place.save()
    repo = jsonify(new_place.to_dict())
    repo.status_code = 201

    return repo

@app_views.route("/places/<place_id>",  methods=["PUT"], strict_slashes=False)
def place_update(place_id):
    """update a place"""
    place_j = request.get_json(silent=True)
    if place_j is None:
        abort(400, 'Not a JSON')
    d_obj = storage.get("Place", str(place_id))
    if d_obj is None:
        abort(404)
    for key, val in place_j.items():
        if key not in ["id", "created_at", "updated_at"]:
            setattr(d_obj, key, val)
    d_obj.save()
    return jsonify(d_obj.to_dict())
