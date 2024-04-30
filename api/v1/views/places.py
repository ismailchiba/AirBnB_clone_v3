#!/usr/bin/python3
"""handle Place operation"""

from flask import jsonify, abort, request
from api.v1.views import app_views, storage
from models.place import Place


@app_views.route("/cities/<city_id>/places", methods=["GET"], strict_slashes=False)
def places_by_city(city_id):
    """retrieves all Places by city"""
    place_list = []
    city_obj = storage.get("City", str(city_id))
    for p_obj in city_obj.places:
        place_list.append(p_obj.to_json())
    return jsonify(place_list)


@app_views.route("/cities/<city_id>/places", methods=["POST"], strict_slashes=False)
def place_create_id(city_id):
    """create a new place using its id"""
    place_json = request.get_json(silent=True)
    if place_json is None:
        abort(400, 'Not a JSON')
    if not storage.get("User", place_json["user_id"]):
        abort(404)
    if not storage.get("City", city_id):
        abort(404)
    if "user_id" not in place_json:
        abort(400, 'Missing user_id')
    if "name" not in place_json:
        abort(400, 'Missing name')

    place_json["city_id"] = city_id

    new_place = Place(**place_json)
    new_place.save()
    resp = jsonify(new_place.to_json())
    resp.status_code = 201

    return resp


@app_views.route("/places/<place_id>",  methods=["GET"], strict_slashes=False)
def get_place_by_id(place_id):
    """gets a Place using it specific id"""
    place_obj = storage.get("Place", str(place_id))
    if place_obj is None:
        abort(404)
    return jsonify(place_obj.to_json())


@app_views.route("/places/<place_id>",  methods=["PUT"], strict_slashes=False)
def put_place(place_id):
    """update a place"""
    place_json = request.get_json(silent=True)
    if place_json is None:
        abort(400, 'Not a JSON')
    place_obj = storage.get("Place", str(place_id))
    if place_obj is None:
        abort(404)

    for key, value in place_json.items():
        if key not in ["id", "created_at", "updated_at", "user_id", "city_id"]:
            setattr(place_obj, key, value)
    place_obj.save()
    return jsonify(place_obj.to_json())


@app_views.route("/places/<place_id>",  methods=["DELETE"],
                 strict_slashes=False)
def place_delete_id(place_id):
    """delete places using it unique id"""
    place_obj = storage.get("Place", str(place_id))
    if place_obj is None:
        abort(404)
    storage.delete(place_obj)
    storage.save()

    return jsonify({})
