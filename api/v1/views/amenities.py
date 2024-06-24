#!/usr/bin/python3
"""Create a new view for Amenity objects that handles all default RESTFul API actions:"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.amenity import Amenity

@app_views.route('/amenities', methods=['GET'], strict_slashes=False)
def amenities_get_all():
    states_dict = []
    for state in storage.all(Amenity).values():
        states_dict.append(state.to_dict())
    return jsonify(states_dict)

@app_views.route('/amenities/<path:amenity_id>', methods=['GET'], strict_slashes=False)
def amenities_get_state(amenity_id):
    state = storage.get(Amenity, amenity_id)
    if state is None:
        abort(404)
    return jsonify(state.to_dict())

@app_views.route('/amenities/<path:amenity_id>', methods=['DELETE'], strict_slashes=False)
def amenities_delete_state(amenity_id):
    if amenity_id is None:
        abort(404)
    state = storage.get(Amenity, amenity_id)
    if state is None:
        abort(404)
    state.delete()
    storage.save()
    return jsonify({})

@app_views.route('/amenities', methods=['POST'], strict_slashes=False)
def amenities_create_state():
    state = request.get_json()
    if type(state) != dict:
        return abort(400, {'message': 'Not a JSON'})
    if 'name' not in state:
        return abort(400, {'message': 'Missing name'})
    buff = Amenity(**state)
    buff.save()
    return jsonify(buff.to_dict()), 201

@app_views.route('/amenities/<path:amenity_id>', methods=['PUT'], strict_slashes=False)
def amenities_update_state(amenity_id):
    if amenity_id is None:
        abort(404)
    state = storage.get(Amenity, amenity_id)
    if state is None:
        abort(404)
    state_req = request.get_json()
    if type(state_req) != dict:
        return abort(400, {'message': 'Not a JSON'})
    for x, y in state_req.items():
        if x not in ["id", "state_id", "created_at", "updated_at"]:
            setattr(state, x, y)
    storage.save()
    return jsonify(state.to_dict()), 200
