#!/usr/bin/python3
""" API """
from flask import jsonify, request
from api.v1.views import app_views
from models import storage
from models.amenity import Amenity


class NotFound(Exception):
    pass


class MethodNotAllowed(Exception):
    pass


class BadRequest(Exception):
    pass


@app_views.route('/amenities', methods=['GET', 'POST'])
@app_views.route('/amenities/<amenity_id>', methods=['GET', 'DELETE', 'PUT'])
def manage_amenities(amenity_id=None):
    """  handler for the amenities """
    handlers = {
            'GET': list_amenities,
            'DELETE': delete_amenity,
            'POST': create_amenity,
            'PUT': edit_amenity,
    }
    if request.method in handlers:
        return handlers[request.method](amenity_id)
    else:
        raise MethodNotAllowed(list(handlers.keys()))


@app_views.route('/amenities', methods=['GET'])
def list_amenities(amenity_id=None):
    """ all amenities"""
    all_amenities = storage.all(Amenity).values()
    if amenity_id:
        res = list(filter(lambda x: x.id == amenity_id, all_amenities))
        if res:
            return jsonify(res[0].to_dict())
        raise NotFound()
    all_amenities = list(map(lambda x: x.to_dict(), all_amenities))
    return jsonify(all_amenities)


@app_views.route('/amenities/<amenity_id>', methods=['DELETE'])
def delete_amenity(amenity_id=None):
    """ delete amenity """
    all_amenities = storage.all(Amenity).values()
    res = list(filter(lambda x: x.id == amenity_id, all_amenities))
    if res:
        storage.delete(res[0])
        storage.save()
        return jsonify({}), 200
    raise NotFound()


@app_views.route('/amenities', methods=['POST'])
def create_amenity(amenity_id=None):
    """ New amenity"""
    data = request.get_json()
    if type(data) is not dict:
        raise BadRequest('Not a JSON')
    if 'name' not in data:
        raise BadRequest('Missing name')
    new_amenity = Amenity(**data)
    new_amenity.save()
    return jsonify(new_amenity.to_dict()), 201


@app_views.route('/amenities/<amenity_id>', methods=['PUT'])
def edit_amenity(amenity_id=None):
    """ update amenity """
    keys_to_ignore = ('id', 'created_at', 'updated_at')
    all_amenities = storage.all(Amenity).values()
    res = list(filter(lambda x: x.id == amenity_id, all_amenities))
    if res:
        data = request.get_json()
        if type(data) is not dict:
            raise BadRequest('Not a JSON')
        old_amenity = res[0]
        for key, value in data.items():
            if key not in keys_to_ignore:
                setattr(old_amenity, key, value)
        old_amenity.save()
        return jsonify(old_amenity.to_dict()), 200
    raise NotFound()
