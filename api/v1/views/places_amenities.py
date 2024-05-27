#!/usr/bin/python3
"""
Route for handling place and amenities linking
"""
from flask import jsonify, abort
from os import getenv
from api.v1.views import app_views, storage


@app_views.route("/places/<place_id>/amenities", methods=["GET"], strict_slashes=False)
def amenity_by_place(place_id):
    """
    get all amenities of a place
    :param place_id: place id
    :return: all amenities
    """
    place = storage.get("Place", place_id)

    if place is None:
        abort(404)

    amenities = [amenity.to_json() for amenity in place.amenities]
    return jsonify(amenities)


@app_views.route("/places/<place_id>/amenities/<amenity_id>", methods=["DELETE"], strict_slashes=False)
def unlink_amenity_from_place(place_id, amenity_id):
    """
    unlinks an amenity from a place
    :param place_id: place id
    :param amenity_id: amenity id
    :return: empty dict or error
    """
    place = storage.get("Place", place_id)
    if place is None:
        abort(404)

    amenity = storage.get("Amenity", amenity_id)
    if amenity is None:
        abort(404)

    if amenity not in place.amenities:
        abort(404)

    if getenv("HBNB_TYPE_STORAGE") == "db":
        place.amenities.remove(amenity)
    else:
        place.amenity_ids.remove(amenity_id)

    place.save()
    return jsonify({}), 200


@app_views.route("/places/<place_id>/amenities/<amenity_id>", methods=["POST"], strict_slashes=False)
def link_amenity_to_place(place_id, amenity_id):
    """
    links an amenity to a place
    :param place_id: place id
    :param amenity_id: amenity id
    :return: Amenity obj added or error
    """
    place = storage.get("Place", place_id)
    if place is None:
        abort(404)

    amenity = storage.get("Amenity", amenity_id)
    if amenity is None:
        abort(404)

    if amenity in place.amenities:
        return jsonify(amenity.to_json())

    if getenv("HBNB_TYPE_STORAGE") == "db":
        place.amenities.append(amenity)
    else:
        place.amenity_ids.append(amenity_id)

    place.save()
    return jsonify(amenity.to_json()), 201
