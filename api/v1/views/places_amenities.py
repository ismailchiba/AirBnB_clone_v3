#!/usr/bin/python3
"""
Handle all default RESTFul API actions.

for linking Place and Amenity objects
"""
from flask import Flask, request, jsonify, abort
from models import storage
from models.place import Place
from models.amenity import Amenity

app = Flask(__name__)


@app.route('/api/v1/places/<place_id>/amenities', methods=['GET'])
def get_place_amenities(place_id):
    """Retrieve the list of all Amenity objects of a Place"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    amenities = place.amenities if storage.__class__.__name__ == 'DBStorage'\
        else [storage.get(Amenity, aid) for aid in place.amenity_ids]
    return jsonify([amenity.to_dict() for amenity in amenities])


@app.route('/api/v1/places/<place_id>/amenities/<amenity_id>',
           methods=['DELETE'])
def delete_place_amenity(place_id, amenity_id):
    """Delete an Amenity object from a Place"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)

    if storage.__class__.__name__ == 'DBStorage':
        if amenity not in place.amenities:
            abort(404)
        place.amenities.remove(amenity)
    else:
        if amenity_id not in place.amenity_ids:
            abort(404)
        place.amenity_ids.remove(amenity_id)

    storage.save()
    return jsonify({})


@app.route('/api/v1/places/<place_id>/amenities/<amenity_id>',
           methods=['POST'])
def link_place_amenity(place_id, amenity_id):
    """Link an Amenity object to a Place"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)

    if storage.__class__.__name__ == 'DBStorage':
        if amenity in place.amenities:
            return jsonify(amenity.to_dict()), 200
        place.amenities.append(amenity)
    else:
        if amenity_id in place.amenity_ids:
            return jsonify(amenity.to_dict()), 200
        place.amenity_ids.append(amenity_id)

    storage.save()
    return jsonify(amenity.to_dict()), 201
