#!/usr/bin/python3
""" Module for Place-Amenity API """


from api.v1.views import app_views, jsonify
from flask import request, abort
import models
from models.place import Place
from models.amenity import Amenity
from models import storage

@app_views.route('/places/<place_id>/amenities', methods=['GET'],
                 strict_slashes=False)
def get_place_amenities(place_id):
    """ Retrieves the list of all Amenity objects of a Place """
    place_obj = storage.get(Place, place_id)
    if place_obj is None:
        abort(404)

    list_amenities_json = []
    
    if models.storage_t == 'db':
        list_amenities = place_obj.amenities
        for amenity in list_amenities:
            list_amenities_json.append(amenity.to_dict())
    else:
        for amenity_id in place_obj.amenity_ids:
            amenity = storage.get(Amenity, amenity_id)
            if amenity is not None:
                list_amenities_json.append(amenity.to_dict())
    return jsonify(list_amenities_json)


@app_views.route('/places/<place_id>/amenities/<amenity_id>',
                 methods=['DELETE'], strict_slashes=False)
def delete_place_amenity(place_id, amenity_id):
    """ Deletes a Amenity object from a Place """
    place_obj = storage.get(Place, place_id)
    if place_obj is None:
        abort(404)

    amenity_obj = storage.get(Amenity, amenity_id)
    if amenity_obj is None:
        abort(404)

    if models.storage_t == 'db':
        # If this amenity is not linked to the place, raise 404
        if amenity_obj not in place_obj.amenities:
            abort(404)
        else:
            place_obj.amenities.remove(amenity_obj)
    else:
        if amenity_id not in place_obj.amenity_ids:
            abort(404)
        else:
            place_obj.amenity_ids.remove(amenity_id)

    storage.save()
    return jsonify({}), 200


@app_views.route('/places/<place_id>/amenities/<amenity_id>',
                  methods=['POST'], strict_slashes=False)
def post_place_amenity(place_id, amenity_id):
    """ Link a Amenity object to a Place """
    place_obj = storage.get(Place, place_id)
    if place_obj is None:
        abort(404)

    amenity_obj = storage.get(Amenity, amenity_id)
    if amenity_obj is None:
        abort(404)

    if models.storage_t == 'db':
        if amenity_obj in place_obj.amenities:
            return jsonify(amenity_obj.to_dict()), 200
        else:
            place_obj.amenities.append(amenity_obj)
            storage.save()
            return jsonify(amenity_obj.to_dict()), 201
    else:
        if amenity_id in place_obj.amenity_ids:
            return jsonify(amenity_obj.to_dict()), 200
        else:
            place_obj.amenity_ids.append(amenity_id)
            storage.save()
            return jsonify(amenity_obj.to_dict()), 201
