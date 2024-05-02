#!/usr/bin/python3
"""
This view is the link between Place objects
and Amenity objects the handles all defualt
RESTFul API actions
"""

from flask import jsonify, make_response, abort
from models import storage, storage_t
from api.v1.views import app_views


@app_views.route('/places/<place_id>/amenities', strict_slashes=False)
def get_amenities(place_id):
    """
    Retrieves tha list of all Amenity objects of Place with the
    specified place_id
    """

    place = storage.get("Place", place_id)

    if place is None:
        abort(404)

    if storage_t == 'db':
        place_obj = [place.to_dict() for place in place.amenities]

        return jsonify(place_obj)
    else:
        place_obj = []
        amenity_ids = place.get('amenity_ids')
        all_places = storage.all("Place")

        for value in all_places.values():
            if value['id'] in amenity_ids:
                place_obj.append(value.to_dict())

        return jsonify(place_obj)


@app_views.rout('/places/<place_id>/amenities/<amenity_id>',
                methods=["DELETE"], strict_slashes=False)
def delete_amenity(place_id, amenity_id):
    """
    Deletes a Amenity object to a Place
    """

    place = storage.get("Place", place_id)

    if place is None:
        abort(404)

    amenity = storage.get("Amenity", amenity_id)

    if amenity is None:
        abort(404)

    if storage_t == 'db':
        amenities = place.amenities

        for value in amenities.values():
            if value.id == amenity_id:
                value.delete()
                storage.save()
                return make_response({}, 200)
        abort(404)

    else:
        amenity_ids = place.get('amenity_ids')

        if amenity_id in amenity_ids:
            amenity_ids.remove(amenity_id)
            place.save()

        abort(404)


@app_views.route('/places/<place_id>/amenities/<amenity_id>',
                 methods=["POST"], strict_slashes=False)
def link_amenity_to_place(place_id, amenity_id):
    """
    This method links a Amenity Object to a Place object with the
    specified place_id and amenity_id
    """

    place = storage.get("Place", place_id)

    if place is None:
        abort(404)

    amenity = storage.get("Amenity", amenity_id)

    if amenity is None:
        abort(404)

    if storage_t == 'db':
        if amenity.to_dict().get('place_id') == place_id:
            return make_response(jsonify(amenity.to_dict), 200)
        else:
            amenity.to_dict()['place_id'] = place_id
            amenity.save()

            return make_response(jsonify(amenity.to_dict()), 201)
    else:
        amenity_ids = place.get('amenity_ids')

        if amenity.id in amenity_ids:
            return make_response(jsonify(amenity.to_dict()), 200)
        else:
            amenity_ids.append(amenity.id)
            amenity.save()

            return make_response(amenity.to_dict(), 201)
