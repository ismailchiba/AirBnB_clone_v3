#!/usr/bin/python3

""" This module contains routes linking places and ameinities """

from models.amenity import Amenity
from models.place import Place
from flask import request, jsonify, make_response, abort
from models import storage
from api.v1.views import app_views


@app_views.route('/places/<place_id>/amenities', methods=['GET'],
                 strict_slashes=False)
def get_place_amenities(place_id):
    """ 
    returns a list of place amenities of place with id
    <place_id>
    """
    place = storage.get('Place', place_id)
    if not place:
        abort(404)
    else:
        amenities = [amenity.to_dict() for amenity in  place.amenities()]
        return jsonify(amenities)


@app_views.route('/places/<place_id>/amenities/<amenity_id>', methods=['GET'],
                 strict_slashes=False)
def delete_place_amenities(place_id, amenity_id):
    """ deletes amenity to a place """
    place = storage.get("Place", place_id)
    amenity = storage.get("Amenity", amenity_id)
    if not amenity:
        abort(404)
    if not place:
        abort(404)
    else:
        for amenity in place.emenities:
            if amenity.id == amenity_id:
                amenity = amenity
                storage.delete(amenity)
                storage.save()
                return make_response(jsonify({}), 201) 
        abort(404)


@app_views.route('/places/<place_id>/amenities/<amenity_id>', methods=['POST'],
                 strict_slashes=False)
def delete_place_amenities(place_id, amenity_id):
    """ adds amenity to a place """
    place = storage.get("Place", place_id)
    amenity = storage.get("Amenity", amenity_id)
    if not amenity:
        abort(404)
    if not place:
        abort(404)
    else:
        if amenity in place.amenities:
            return make_response(jsonify(amenity.to_dict()), 200)
        setattr(place, "place_id", place.id)
        place.save()
        return make_response(jsonify(place.to_dict()), 201)
