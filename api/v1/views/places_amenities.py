#!/usr/bin/python3
""" view for the link between Place objects and Amenity objects """

from flask import abort, request, make_response, jsonify
from models import storage
from models.place import Place
from models.amenity import Amenity
from os import getenv
from api.v1.views import app_views


@app_views.route('/places/<place_id>/amenities', methods=['GET'],
                 strict_slashes=False)
def get_places_amenities(place_id):
    """ Retrieves the list of all Amenity objects of a Place """
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)

    if getenv('HBNB_TYPE_STORAGE') == 'db':
        amenities = [amenity.to_dict() for amenity in place.amenities]
    else:
        amenities = [storage.get(Amenity, amenity_id).to_dict()
                     for amenity_id in place.amenity_ids]
    return jsonify(amenities)


@app_views.route('/places/<place_id>/amenities/<amenity_id>', methods=['GET'],
                 strict_slashes=False)
def delete_place_amenity(place_id, amenity_id):
    """ Delete """
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)

    if getenv('HBNB_TYPE_STORAGE') == 'db':
        amenities = storage.all(Amenity).values()
        if amenity not in place.amenities:
            abort(404)
        place.amenities.delete(amenity)
    else:
        amenities = storage.get(Amenity, amenity_id)
        if amenity_id not in place.amenities:
            place.amenities.remove(amenity_id)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/places/<place_id>/amenities/<amenity_id>', methods=['POST'],
                 strict_slashes=False)
def link_place_amenity(place_id, amenity_id):
    """ Link a Amenity object to a Place """
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)

    if getenv('HBNB_TYPE_STORAGE') == 'db':
        if amenity in place.amenities:
            return make_response(jsonify(amenity.to_dict()), 200)
        else:
            place.amenities.append(amenity)
    else:
        if amenity_id in place.amenity_ids:
            return make_response(jsonify(amenity.to_dict()), 200)
        else:
            place.amenity_ids.append(amenity_id)
    storage.save()
    return make_response(jsonify(amenity.to_dict()), 201)
