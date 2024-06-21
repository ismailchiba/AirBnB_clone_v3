#!/usr/bin/python3
"""
city restful api
"""
from flask import jsonify
from flask import request
from flask import abort
from models.amenity import Amenity
from models import storage
from api.v1.views import app_views


@app_views.route('/amenities/',
                 strict_slashes=False, methods=['GET'])
def get_all_amenities():
    """Retreive all Amenities"""
    amenities = storage.all(Amenity)
    return jsonify([i.to_dict() for i in amenities.values()])


@app_views.route('/amenities/<amenity_id>',
                 strict_slashes=False, methods=['GET'])
def get_amenityebyId(amenity_id):
    """retrieve amenity by its id"""
    amenities = storage.all(Amenity)
    for k, v in amenities.items():
        if v.to_dict().get('id') == amenity_id:
            return jsonify(v.to_dict())
    return (abort(404))


@app_views.route('/amenities/',
                 strict_slashes=False, methods=['POST'])
def post_amenity():
    """create a an amenity"""
    try:
        data = request.get_json()
    except:
        return (abort(400, 'Not a JSON'))
    if not data:
        return (abort(400, 'Not a JSON'))
    elif 'name' not in data.keys():
        return (abort(400, 'Missing name'))
    elif not data['name']:
        return (abort(400, 'Missing name'))
    else:
        amenity = Amenity(**data)
        storage.new(amenity)
        storage.save()
        return jsonify(amenity.to_dict()), 201


@app_views.route('/amenities/<amenity_id>/',
                 strict_slashes=False, methods=['PUT'])
def update_amenity(amenity_id):
    """update city in state"""
    try:
        data = request.get_json()
    except:
        return (abort(400, 'Not a JSON'))
    if not data:
        abort(400, 'Not a JSON')
    if 'name' not in data:
        abort(400, 'Missing name')
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        return (abort(404))
    ignore_keys = ['id', 'state_id', 'created_at', 'updated_at']
    for k, v in data.items():
        if k not in ignore_keys:
            setattr(amenity, k, v)
    amenity.save()
    return jsonify(amenity.to_dict()), 200


@app_views.route('/amenities/<amenity_id>/',
                 strict_slashes=False, methods=['DELETE'])
def delete_amenity(amenity_id):
    """delete the amenity by its id"""
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)
    storage.delete(amenity)
    storage.save()
    return jsonify({}), 200
