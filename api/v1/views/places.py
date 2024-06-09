#!/usr/bin/python3
""" objects that handles all default RestFul API actions for Places"""
from api.v1.views import app_views
from flask import jsonify, abort, request, make_response
from models import storage
from models.place import Place


@app_views.route("/places", methods=["GET"], strict_slashes=False)
def get_place():
    """Retrieves the list of all Place objects"""
    all_places = storage.all(Place).values()
    list_place = []
    for place in all_places:
        list_place.append(place.to_dict())
    return jsonify(list_place)


@app_views.route("/places/<place_id>", methods=["GET"], strict_slashes=False)
def get_place_id(place_id):
    """Retrieves a Place by id"""
    place = storage.get(place, place_id)
    if not place:
        abort(404)

    return jsonify(place.to_dict())


@app_views.route("/places/<place_id>", methods=["DELETE"], strict_slashes=False)
def delete_place_id(place_id):
    """Deletes a Place object by id"""
    place = storage.get(place, place_id)
    if not place:
        abort(404)
    storage.delete(place)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route("/places", methods=["POST"], strict_slashes=False)
def create_place():
    """Creates a Place"""
    if not request.get_json():
        abort(400, description="Not a JSON")
    if not "name" in request.json():
        abort(400, "Missing name")

    place = request.json()
    instance = Place(**place)
    storage.new(instance)
    storage.save()

    return make_response(jsonify(place), 201)


@app_views.route("/places/<place_id>", methods=["PUT"], strict_slashes=False)
def update_place(place_id):
    """Updates a Place object by id"""
    if not request.get_json():
        abort(400, description="Not a JSON")
    if not storage.get(place, place_id):
        abort(404)

    place = storage.get(place, place_id)
    place_data = request.get_json()
    ignore_keys = ["id", "created_at", "updated_at"]
    for key, value in place_data.items():
        if key not in ignore_keys:
            setattr(place, key, value)
    storage.save()

    return make_response(jsonify(place), 200)
