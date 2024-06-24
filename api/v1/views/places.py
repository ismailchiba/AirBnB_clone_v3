#!/usr/bin/python3
"""cities module"""

from flask import jsonify, abort, request
from api.v1.views import app_views, storage
from models.place import Place
from models.city import City
from models.user import User

@app_views.route('/cities/<city_id>/places', methods=['GET'],
                 strict_slashes=False)
def get_place_by_city(city_id):
    """get places"""
    places = []
    state_objects = storage.get("City", city_id)
    if state_objects is None:
        abort(404)
    for city in state_objects.places:
        if place.city_id == city_id:
            places.append(place.to_json())
    return jsonify(places)


@app_views.route('/cities/<city_id>/places', methods=['POST'],
                 strict_slashes=False)
def post_place(city_id):
    """post place"""
    new_place = request.get_json(silent=True)
    if new_place is None:  # check if json post request is valid
        abort(404, "Not a JSON")
    if not storage.get("City", city_id):  # check if state_id exists
        abort(404)
    if 'user_id' not in new_place:
       abort(400, 'Missing user_id')
    state_objects = storage.get("User", new_place.get("user_id"))
    if state_objects is None:
        abort(404)
    if 'name' not in new_place:
        abort(400, 'Missing name')
    place = Place(**new_place)
    setattr(place, 'city_id', city_id)
    place.save()
    return jsonify(place.to_dict()), 201


@app_views.route("/places/<place_id>", methods=["GET"], strict_slashes=False)
def get_place_by_id(place_id):
    """get place by id"""
    place_object = storage.get("Place", place_id)
    if place_object is None:
        abort(404)
    return jsonify(place_object.to_dict())


@app_views.route("places/<place_id>",  methods=["PUT"], strict_slashes=False)
def put_place(place_id):
    """put place by id """
    place_update = request.get_json(silent=True)
    if place_update is None:
        abort(400, 'Not a JSON')
    place_object = storage.get("Place", place_id)
    if place_object is None:
        abort(404)
    for key, val in place_update.items():
        if key not in ["id", "user_id", "city_id", "created_at", "updated_at"]:
            setattr(place_object, key, val)
    place_object.save()
    return jsonify(place_object.to_dict())


@app_views.route("/places/<place_id>",  methods=["DELETE"],
                 strict_slashes=False)
def place_delete_by_id(city_id):
    """delete place by id"""
    place_object = storage.get("Place", place_id)
    if place_object is None:
        abort(404)
    storage.delete(place_object)
    storage.save()
    return jsonify({})
