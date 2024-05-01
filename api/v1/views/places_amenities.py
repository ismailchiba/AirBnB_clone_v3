#!/usr/bin/python3
"""Create a view for Place-Amenity relationships"""

from api.v1.views import app_views
from flask import jsonify, abort, request
from models.place import Place
from models.amenity import Amenity
from models import storage

@app_views.route('/places/<place_id>/amenities', methods=['GET'])
def get_place_amenities(place_id):
    """Retrieves the list of all Amenity objects of a Place"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    
    amenities = [amenity.to_dict() for amenity in place.amenities]
    return jsonify(amenities)

@app_views.route('/places/<place_id>/amenities/<amenity_id>', methods=['DELETE'])
def delete_place_amenity(place_id, amenity_id):
    """Deletes an Amenity object from a Place"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)

    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)

    if amenity not in place.amenities:
        abort(404)

    place.amenities.remove(amenity)
    storage.save()
    return jsonify({}), 200

@app_views.route('/places/<place_id>/amenities/<amenity_id>', methods=['POST'])
def link_amenity_to_place(place_id, amenity_id):
    """Links an Amenity object to a Place"""

    place = storage.get(Place, place_id)
    if not place:
        abort(404)

    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)

    if amenity in place.amenities:
        return jsonify(amenity.to_dict()), 200

    place.amenities.append(amenity)
    storage.save()
    return jsonify(amenity.to_dict()), 201


@app_views.route('/places/<place_id>/amenities/<amenity_id>', methods=['PUT'])
def update_place_amenity(place_id, amenity_id):
    """Updates the link between a Place and an Amenity"""

    answer = models.storage.get("Amenity", amenity_id)
    if answer:
        if not request.json:
            return jsonify({"error": "Not a JSON"}), 400
        for k, v in request.get_json().items():
            if k not in ['id', 'user_id',
                         'created_at', 'updated_at', 'state_id']:
                setattr(answer, k, v)
        answer.save()
        return jsonify(answer.to_dict()), 200
    abort(404)
