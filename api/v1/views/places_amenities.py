#!/usr/bin/python3
"""
Route for handling place and amenities linking
"""
from flask import jsonify, abort
from os import getenv

from api.v1.views import app_views, storage
from models.amenity import Amenity
from models.place import Place


@app_views.route("/places/<place_id>/amenities", methods=["GET"], strict_slashes=False)
def get_amenities_by_place(place_id):
    """
    Get all amenities of a place
    :param place_id: Place ID
    :return: JSON response containing all amenities
    """
    place = storage.get("Place", place_id)
    if place is None:
        abort(404)

    amenities = [amenity.to_json() for amenity in place.amenities]
    return jsonify(amenities)


@app_views.route("/places/<place_id>/amenities/<amenity_id>", methods=["DELETE"], strict_slashes=False)
def unlink_amenity_from_place(place_id, amenity_id):
    """
    Unlinks an amenity from a place
    :param place_id: Place ID
    :param amenity_id: Amenity ID
    :return: Empty JSON response or error
    """
    place = storage.get("Place", place_id)
    if place is None:
        abort(404)

    amenity = storage.get("Amenity", amenity_id)
    if amenity is None:
        abort(404)

    if amenity not in place.amenities:
        abort(404)

    place.amenities.remove(amenity)
    place.save()
    
    return jsonify({}), 200


@app_views.route("/places/<place_id>/amenities/<amenity_id>", methods=["POST"], strict_slashes=False)
def link_amenity_to_place(place_id, amenity_id):
    """
    Links an amenity with a place
    :param place_id: Place ID
    :param amenity_id: Amenity ID
    :return: JSON response containing the linked Amenity object or error
    """
    place = storage.get("Place", place_id)
    if place is None:
        abort(404)

    amenity = storage.get("Amenity", amenity_id)
    if amenity is None:
        abort(404)

    if amenity in place.amenities:
        return jsonify(amenity.to_json())

    place.amenities.append(amenity)
    place.save()
    
    return jsonify(amenity.to_json()), 201
