#!/usr/bin/python3
"""Place-Amenities objects view"""
from flask import abort, jsonify, request
from models import storage, storage_t
from models.place import Place
from models.amenity import Amenity
from models.user import User
from api.v1.views import app_views


@app_views.route("/places/<place_id>/amenities", methods=["GET"],
                 strict_slashes=False)
def get_all_amenities(place_id):
    """List Place's amenities"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)

    place_amenities = [amenity.to_dict()
                       for amenity in place.amenities]
    return jsonify(place_amenities)


@app_views.route("/places/<place_id>/amenities/<amenity_id>",
                 methods=["DELETE"], strict_slashes=False)
def removing_amenity(place_id, amenity_id):
    """Delete Amenity for a Place"""
    place = storage.get(Place, place_id)
    amenity = storage.get(Amenity, amenity_id)
    if not place or not amenity:
        abort(404)
    if storage_t == 'db':
        if amenity in place.amenities:
            place.amenities.remove(amenity)
            storage.save()
            return jsonify({}), 200
        abort(404)
    amenity_index = place.amenity_ids.index(amenity.id)
    place.amenity_ids.pop(amenity_index)
    storage.save()
    return jsonify({}), 200


@app_views.route("/places/<place_id>/amenities/<amenity_id>",
                 methods=["POST"])
def link_amenity_to_place(place_id, amenity_id):
    """Link Amenity to a Place"""
    place = storage.get(Place, place_id)
    amenity = storage.get(Amenity, amenity_id)
    if not place or not amenity:
        abort(404)

    if storage_t == 'db':
        if amenity in place.amenities:
            return jsonify(amenity.to_dict()), 200
        place.amenities.append(amenity)
    else:
        if amenity.id in place.amenity_ids:
            return jsonify(amenity.to_dict()), 200
        place.amenity_ids.append(amenity.id)

    storage.save()
    return jsonify(amenity.to_dict()), 201
