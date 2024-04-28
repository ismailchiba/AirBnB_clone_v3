#!/usr/bin/python3
"""Place Amenities route handler"""

from api.v1.views import app_views
from flask import abort, make_response, jsonify
from models import storage
import models
from models.amenity import Amenity
from models.place import Place


@app_views.route("/places/<place_id>/amenities", strict_slashes=False,
                 methods=["GET"])
def get_amenities(place_id):
    """ get amenities by place ID"""
    amenity_list = []
    amenities = []
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    else:
        if models.storage_t == 'db':
            amenities = place.amenities
        else:
            amenities = place.amenity_ids
        for a in amenities:
            amenity_list.append(a.to_dict())
    return jsonify(amenity_list)


@app_views.route("/places/<place_id>/amenities/<amenity_id>",
                 strict_slashes=False, methods=["DELETE"])
def delete_amenity(place_id, amenity_id):
    """ delete amenity by place"""
    amenities = []
    place = storage.get(Place, place_id)
    amenity = storage.get(Amenity, amenity_id)
    if place is None or amenity is None:
        abort(404)
    if models.storage_t == 'db':
        amenities = place.amenities
    else:
        amenities = place.amenity_ids
    if amenity not in amenities:
        abort(404)
    storage.delete(amenity)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route("/places/<place_id>/amenities/<amenity_id>",
                 strict_slashes=False, methods=["POST"])
def link_amenity_to_place(place_id, amenity_id):
    """ link amenity to place by place_id"""
    amenities = []
    place = storage.get(Place, place_id)
    amenity = storage.get(Amenity, amenity_id)
    if place is None or amenity is None:
        abort(404)
    if models.storage_t == 'db':
        amenities = place.amenities
    else:
        amenities = place.amenity_ids
    if amenity in amenities:
        return make_response(jsonify(amenity.to_dict()), 200)
    else:
        amenities.append(amenity)
        storage.save()
        return make_response(jsonify(amenity.to_dict()), 201)
