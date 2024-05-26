#!/usr/bin/python3
"""
This module defines Flask routes to provide API endpoints
that link between Place and Amenity objects.
"""
from math import e
from os import environ

from flask import abort, jsonify

from api.v1.views import app_views
from models import storage
from models.amenity import Amenity
from models.place import Place

api_route_1 = "/places/<string:place_id>/amenities"
api_route_2 = "/places/<string:place_id>/amenities/<string:amenity_id>"

storage_type = environ.get("HBNB_TYPE_STORAGE")

@app_views.route(api_route_1, methods=["GET"], strict_slashes=False)
def get_place_amenities(place_id):
    """
    Retrieve the amenities of a place.

    Args:
        place_id (str): The ID of the place.

    Returns:
        tuple: A tuple containing a JSON response with the amenities
        list and a status code.

    Raises:
        404: If the place with the given ID does not exist.
    """
    place = storage.get(Place, place_id)

    if place is None:
        abort(404)

    amenities = []

    if storage_type == "db":
        for amenity in place.amenities:
            amenities.append(amenity.to_dict())
    else:
        for amenity_id in place.amenity_ids:
            amenity = storage.get(Amenity, amenity_id)
            if amenity:
                amenities.append(amenity.to_dict())

    response = jsonify(amenities), 200

    return response


@app_views.route(api_route_2, methods=["DELETE"], strict_slashes=False)
def delete_amenity(place_id, amenity_id):
    """
    Delete an amenity from a place.

    Args:
        place_id (str): The ID of the place.
        amenity_id (str): The ID of the amenity to be deleted.

    Returns:
        dict: An empty dictionary.

    Raises:
        404: If the place or the amenity is not found.

    """
    place = storage.get(Place, place_id)

    if place is None:
        abort(404)

    amenity = storage.get(Amenity, amenity_id)

    if not amenity:
        abort(404)

    if storage_type == "db":
        if amenity not in place.amenities:
            abort(404)
        place.amenities.remove(amenity)
    else:
        if amenity_id not in place.amenity_ids:
            abort(404)
        place.amenity_ids.remove(amenity_id)

    storage.save()

    return jsonify({})


@app_views.route(api_route_2, methods=["POST"], strict_slashes=False)
def link_amenity_to_place(place_id, amenity_id):
    """
    Link an amenity to a place.

    Args:
        place_id (str): The ID of the place.
        amenity_id (str): The ID of the amenity.

    Returns:
        tuple: A tuple containing the JSON response and the
        HTTP status code.

    Raises:
        HTTPException: If the place or amenity is not found.

    """
    place = storage.get(Place, place_id)

    if place is None:
        abort(404)

    amenity = storage.get(Amenity, amenity_id)

    if not amenity:
        abort(404)

    if storage_type == "db":
        if amenity in place.amenities:
            return jsonify(amenity.to_dict()), 200
        else:
            place.amenities.append(amenity)
    else:
        if amenity_id in place.amenity_ids:
            return jsonify(amenity.to_dict()), 200
        else:
            place.amenity_ids.append(amenity_id)

    storage.save()
    return jsonify(amenity.to_dict()), 201
