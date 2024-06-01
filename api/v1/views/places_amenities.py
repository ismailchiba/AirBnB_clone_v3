#!/usr/bin/python3
"""
Handling RESTFUL APIs actions for
Place objects and Amenity objects
"""

from api.v1.views import app_views
from flask import abort, jsonify
from models import storage
from models.place import Place
from models.amenity import Amenity
from os import getenv


@app_views.route("/places/<place_id>/amenities", methods=["GET"],
                 strict_slashes=False)
def place_amenities(place_id):
    """
    Returning the amenities list
    of a specific place
    """

    place = storage.get(Place, place_id)

    if not place:
        abort(404)

    amenities_list = [amenity.to_dict() for amenity in place.amenities]

    return jsonify(amenities_list), 200


@app_views.route("/places/<place_id>/amenities/<amenity_id>",
                 methods=["DELETE"], strict_slashes=False)
def delete_place_amenity(place_id, amenity_id):
    """
    Function that deletes an amenity
    in a specific place obejct of its id
    """

    place = storage.get(Place, place_id)
    amenity = storage.get(Amenity, amenity_id)

    if not place or not amenity:
        abort(404)

    if amenity not in place.amenities:
        abort(404)

    if getenv("HBNB_TYPE_STORAGE") == "db":
        place.amenities.remove(amenity)
        place.save()
    else:
        place.amenity_id.remove(amenity_id)

    return jsonify({}), 200


@app_views.route("/places/<place_id>/amenities/<amenity_id>",
                 methods=["POST"], strict_slashes=False)
def add_amenity_to_place(place_id, amenity_id):
    """
    Adding amenity to specific 
    place obejct with its id
    """

    place = storage.get(Place, place_id)
    amenity = storage.get(Amenity, amenity_id)

    if not place or not amenity:
        abort(404)

    if amenity in place.amenities:
        return jsonify(amenity.to_dict()), 200

    if getenv("HBNB_TYPE_STORAGE") == "db":
        place.amenities.append(amenity)
        place.save()
    else:
        place.amenity_id.append(amenity_id)

    return jsonify(amenity.to_dict()), 201
