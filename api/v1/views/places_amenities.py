#!/usr/bin/python3
"""
Routes for handling place and amenities linking.
"""

from flask import jsonify, abort
from os import getenv

from api.v1.views import app_views, storage


@app_views.route("/places/<place_id>/amenities", methods=["GET"], strict_slashes=False)
def get_amenities_by_place(place_id):
    """
    Retrieves all amenities associated with a place.
    """
    place = storage.get("Place", place_id)

    if not place:
        abort(404)

    amenities_list = [amenity.to_json() for amenity in place.amenities]
    return jsonify(amenities_list)


@app_views.route("/places/<place_id>/amenities/<amenity_id>", methods=["DELETE"], strict_slashes=False)
def unlink_amenity_from_place(place_id, amenity_id):
    """
    Unlinks an amenity from a place.
    """
    place = storage.get("Place", place_id)
    amenity = storage.get("Amenity", amenity_id)

    if not place or not amenity:
        abort(404)

    if amenity not in place.amenities:
        abort(404)

    if getenv("HBNB_TYPE_STORAGE") == "db":
        place.amenities.remove(amenity)
    else:
        place.amenity_ids.remove(amenity.id)

    place.save()

    return jsonify({}), 200


@app_views.route("/places/<place_id>/amenities/<amenity_id>", methods=["POST"], strict_slashes=False)
def link_amenity_to_place(place_id, amenity_id):
    """
    Links an amenity to a place.
    """
    place = storage.get("Place", place_id)
    amenity = storage.get("Amenity", amenity_id)

    if not place or not amenity:
        abort(404)

    if amenity in place.amenities:
        return jsonify(amenity.to_json()), 200

    if getenv("HBNB_TYPE_STORAGE") == "db":
        place.amenities.append(amenity)
    else:
        place.amenity_ids.append(amenity.id)

    place.save()

    return jsonify(amenity.to_json()), 201
