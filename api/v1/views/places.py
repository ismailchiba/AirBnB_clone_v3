#!/usr/bin/python3
"""
Routes for handling Place objects and operations.
"""

from flask import jsonify, abort, request
from api.v1.views import app_views, storage
from models.place import Place


@app_views.route("/cities/<city_id>/places", methods=["GET"], strict_slashes=False)
def get_places_by_city(city_id):
    """
    Retrieves all Place objects by city ID.
    """
    place_list = [place.to_json() for place in storage.get("City", city_id).places]
    return jsonify(place_list)


@app_views.route("/cities/<city_id>/places", methods=["POST"], strict_slashes=False)
def create_place(city_id):
    """
    Creates a new Place object.
    """
    place_json = request.get_json(silent=True)
    if not place_json:
        abort(400, 'Not a JSON')

    if "user_id" not in place_json:
        abort(400, 'Missing user_id')

    if "name" not in place_json:
        abort(400, 'Missing name')

    if not storage.get("User", place_json["user_id"]):
        abort(404)

    if not storage.get("City", city_id):
        abort(404)

    place_json["city_id"] = city_id
    new_place = Place(**place_json)
    new_place.save()
    return jsonify(new_place.to_json()), 201


@app_views.route("/places/<place_id>", methods=["GET"], strict_slashes=False)
def get_place_by_id(place_id):
    """
    Retrieves a specific Place object by ID.
    """
    place = storage.get("Place", place_id)
    if not place:
        abort(404)
    return jsonify(place.to_json())


@app_views.route("/places/<place_id>", methods=["PUT"], strict_slashes=False)
def update_place(place_id):
    """
    Updates a specific Place object by ID.
    """
    place_json = request.get_json(silent=True)
    if not place_json:
        abort(400, 'Not a JSON')

    place = storage.get("Place", place_id)
    if not place:
        abort(404)

    for key, value in place_json.items():
        if key not in ["id", "created_at", "updated_at", "user_id", "city_id"]:
            setattr(place, key, value)

    place.save()
    return jsonify(place.to_json())


@app_views.route("/places/<place_id>", methods=["DELETE"], strict_slashes=False)
def delete_place(place_id):
    """
    Deletes a Place object by ID.
    """
    place = storage.get("Place", place_id)
    if not place:
        abort(404)

    storage.delete(place)
    storage.save()
    return jsonify({}), 200
