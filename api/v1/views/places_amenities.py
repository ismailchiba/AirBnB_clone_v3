#!/usr/bin/python3
"""places amenities"""
from flask import abort, jsonify, request, make_response
from models import storage
from models.amenity import Amenity
from api.v1.views import app_views


@app_views.route("/places/<place_id>/amenities", methods=["GET"])
def place_amenities(place_id):
    """Getting a list of amenities for a place."""
    place = storage.get("Place", place_id)
    if place is None:
        abort(404)
    return jsonify([amenity.to_dict() for amenity in place.amenities])


@app_views.route(
    "/places/<place_id>/amenities/<amenity_id>",
    methods=["POST"]
)
def post_place_amenities(place_id, amenity_id):
    """Link an amenity to a place."""
    place = storage.get("Place", place_id)
    amenity = storage.get("Amenity", amenity_id)
    if place is None or amenity is None:
        abort(404)

    if amenity in place.amenities:
        return make_response(jsonify(amenity.to_dict()), 200)

    place.amenities.append(amenity)
    place.save()
    return make_response(jsonify(amenity.to_dict()), 201)


@app_views.route(
    "/places/<place_id>/amenities/<amenity_id>",
    methods=["DELETE"]
)
def delete_place_amenity(place_id, amenity_id):
    """Unlink an amenity from a place."""
    place = storage.get("Place", place_id)
    amenity = storage.get("Amenity", amenity_id)
    if place is None or amenity is None:
        abort(404)

    if amenity not in place.amenities:
        abort(404)

    place.amenities.remove(amenity)
    place.save()
    return jsonify({}), 200
