#!/usr/bin/python3
"""
Module that handles all default RESTful API actions for
Places/Amenities class
"""

from api.v1.views import app_views
from flask import jsonify, abort
import models
from models import storage
from models.amenity import Amenity
from models.place import Place


@app_views.route(
    "/places/<place_id>/amenities", methods=["GET"], strict_slashes=False
)
def get_place_amenity(place_id):
    """retrieves the list of amenity objects of a particular place"""
    place = storage.get(Place, place_id)

    if place is None:
        abort(404)

    amenities = [amenity.to_dict() for amenity in place.amenities]
    return jsonify(amenities)


@app_views.route("/places/<place_id>/amenities/<amenity_id>", methods=["POST"])
def create_place_amenity(place_id, amenity_id):
    """creates/links an amenity object to a place"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)

    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)

    if models.storage_t == "db":
        if amenity in place.amenities:
            return jsonify(amenity.to_dict()), 200
        place.amenities.append(amenity)
    else:
        if amenity_id in place.amenity_ids:
            return jsonify(amenity.to_dict()), 200
        place.amenity_ids.append(amenity_id)

    storage.save()
    return jsonify(amenity.to_dict()), 201


@app_views.route(
    "/places/<place_id>/amenities/<amenity_id>", methods=["DELETE"]
)
def delete_place_amenity(place_id, amenity_id):
    """deletes/unlinks an amenity to a place"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)

    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)

    if models.storage_t == "db":
        if amenity not in place.amenities:
            abort(404)
        place.amenities.remove(amenity)
        storage.save()
        return jsonify({}), 200
    else:
        if amenity_id not in place.amenity_ids:
            abort(404)
        place.amenity_ids.remove(amenity_id)
        storage.save()
        return jsonify({}), 200
