#!/usr/bin/python3
"""Endpoints for managing amenities associated with places"""
import os
from flask import abort, jsonify, request
from models import storage
from models.amenity import Amenity
from api.v1.views import app_views


@app_views.route("/places/<place_id>/amenities", methods=["GET"])
def get_place_amenities(place_id):
    """
    Retrieves the list of amenities associated with a specific place.

    Args:
        place_id (str): The ID of the place.

    Returns:
        JSON: A JSON response containing the list of amenities.
    """
    place = storage.get("Place", place_id)

    if place is None:
        abort(404)
    return jsonify([a.to_dict() for a in place.amenities])


@app_views.route(
    "/places/<place_id>/amenities/<amenity_id>",
    methods=["POST"]
)
def add_amenity_to_place(place_id, amenity_id):
    """
    Adds an amenity to a specific place.

    Args:
        place_id (str): The ID of the place.
        amenity_id (str): The ID of the amenity.

    Returns:
        JSON: A JSON response containing the added amenity.
    """
    place = storage.get("Place", place_id)
    amenity = storage.get("Amenity", amenity_id)
    exists = False
    if place is None or amenity is None:
        abort(404)

    if os.getenv("HBNB_TYPE_STORAGE") == "db":
        if amenity in place.amenities:
            exists = True
        else:
            place.amenities.append(amenity)
    else:
        if amenity.id in place.amenity_ids:
            exists = True
        else:
            place.amenity_ids.append(amenity.id)

    place.save()
    return jsonify(amenity.to_dict()), (200 if exists else 201)


@app_views.route(
    "/places/<place_id>/amenities/<amenity_id>",
    methods=["DELETE"]
)
def remove_amenity_from_place(place_id, amenity_id):
    """
    Removes an amenity from a specific place.

    Args:
        place_id (str): The ID of the place.
        amenity_id (str): The ID of the amenity.

    Returns:
        JSON: A JSON response indicating success.
    """
    place = storage.get("Place", place_id)
    amenity = storage.get("Amenity", amenity_id)
    exists = False
    if place is None or amenity is None:
        abort(404)

    if os.getenv("HBNB_TYPE_STORAGE") == "db":
        if amenity not in place.amenities:
            abort(404)
        place.amenities.remove(amenity)
    else:
        if amenity.id not in place.amenity_ids:
            abort(404)
        place.amenity_ids.remove(amenity.id)
    place.save()
    return jsonify({}), 200
