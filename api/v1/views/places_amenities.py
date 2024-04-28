#!/usr/bin/python3
"""review"""
from api.v1.views import app_views
from flask import jsonify, request, abort, make_response
from models import storage
from models.place import Place
from models.amenity import Amenity


@app_views.route(
    'places/<place_id>/amenities',
    methods=['GET'],
    strict_slashes=False
)
def get_places_amenities(place_id):
    """get all places amenities"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    all_amenity = [i.to_dict() for i in place.amenities]
    return jsonify(all_amenity)


@app_views.route(
    '/places/<place_id>/amenities/<amenity_id>',
    methods=['DELETE'],
    strict_slashes=False
)
def delete_place_amenity(place_id, amenity_id):
    """delete place and amenity from id"""
    i = storage.get(Place, place_id)
    if i is None:
        abort(404)
    x = storage.get(Amenity, amenity_id)
    if x is None:
        abort(404)
    if x not in i.amenities:
        abort(404)
    i.amenities.remove(x)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route(
    '/places/<place_id>/amenities/<amenity_id>',
    methods=['POST'],
    strict_slashes=False
)
def create_place_amenity(place_id, amenity_id):
    """create place amenity"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    if amenity in place.amenities:
        return make_response(jsonify(amenity.to_dict()), 200)
    place.amenities.append(amenity)
    storage.save()
    return make_response(jsonify(amenity.to_dict()), 201)
