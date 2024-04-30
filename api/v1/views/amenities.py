#!/usr/bin/python3
<<<<<<< HEAD
""" Module that manages all default RestFul API actions for Facilities"""
from models.amenity import Amenity as Facility
from models import storage
from api.v1.views import app_views
from flask import abort, jsonify, make_response, request
from flasgger.utils import swag_from


@app_views.route('/facilities', methods=['GET'], strict_slashes=False)
@swag_from('documentation/facility/all_facilities.yml')
def get_facilities():
    """
    Fetches a list of all facilities
    """
    all_facilities = storage.all(Facility).values()
    facilities_list = []
    for facility in all_facilities:
        facilities_list.append(facility.to_dict())
    return jsonify(facilities_list)


@app_views.route('/facilities/<facility_id>/', methods=['GET'],
                 strict_slashes=False)
@swag_from('documentation/facility/get_facility.yml', methods=['GET'])
def get_facility(facility_id):
    """ Fetches a facility """
    facility = storage.get(Facility, facility_id)
    if not facility:
        abort(404)

    return jsonify(facility.to_dict())


@app_views.route('/facilities/<facility_id>', methods=['DELETE'],
                 strict_slashes=False)
@swag_from('documentation/facility/delete_facility.yml', methods=['DELETE'])
def delete_facility(facility_id):
    """
    Removes a facility  Object
    """

    facility = storage.get(Facility, facility_id)

    if not facility:
        abort(404)

    storage.delete(facility)
    storage.save()

    return make_response(jsonify({}), 200)


@app_views.route('/facilities', methods=['POST'], strict_slashes=False)
@swag_from('documentation/facility/post_facility.yml', methods=['POST'])
def post_facility():
    """
    Creates a facility
    """
    if not request.get_json():
        abort(400, description="Not a JSON")

    if 'name' not in request.get_json():
        abort(400, description="Missing name")

    payload = request.get_json()
    instance = Facility(**payload)
    instance.save()
    return make_response(jsonify(instance.to_dict()), 201)


@app_views.route('/facilities/<facility_id>', methods=['PUT'],
                 strict_slashes=False)
@swag_from('documentation/facility/put_facility.yml', methods=['PUT'])
def put_facility(facility_id):
    """
    Updates a facility
    """
    if not request.get_json():
        abort(400, description="Not a JSON")

    ignore = ['id', 'created_at', 'updated_at']

    facility = storage.get(Facility, facility_id)

    if not facility:
        abort(404)

    payload = request.get_json()
    for key, value in payload.items():
        if key not in ignore:
            setattr(facility, key, value)
    storage.save()
    return make_response(jsonify(facility.to_dict()), 200)
=======
"""return JSON """
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.state import State
from models.city import City
from models.place import Place
from models.review import Review
from models.amenity import Amenity
from models.user import User


@app_views.route('/amenities', methods=['GET'], strict_slashes=False)
def get_amenities():
    amenity_api = []
    amenities = storage.all(State).values()
    for amenity in amenities:
        amenity_api.append(amenity.to_dict())
    return jsonify(amenity_api)


@app_views.route('/amenities/<amenity_id>', methods=['GET'], strict_slashes=False)
def get_amenity_by_id(amenity_id):
    amenity = storage.get(State, amenity_id)
    if amenity:
        amenity_api = amenity.to_dict()
        return jsonify(amenity_api)
    else:
        from api.v1.app import not_found
        return not_found(404)


@app_views.route('/amenities/<amenity_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_amenity_by_id(amenity_id):
    amenity = storage.get(State, amenity_id)
    if amenity:
        storage.delete(amenity)
        storage.save()
        return jsonify({}), 200
    else:
        abort(404)


@app_views.route('/amenities', methods=['POST'], strict_slashes=False)
def post_amenity_by_name():
    if 'name' not in request.get_json():
        abort(400, 'Missing name')
    if not request.get_json():
        abort(400, 'Not a JSON')

    data_request = request.get_json()
    data = data_request['name']
    obj = State(name=data)
    obj.save()
    return jsonify(obj.to_dict()), 201


@app_views.route('/amenities/<amenity_id>', methods=['PUT'], strict_slashes=False)
def put_amenity_by_id(amenity_id):
    if not request.get_json():
        abort(400, 'Not a JSON')
    amenity = storage.get(State, amenity_id)
    if amenity:
        data_request = request.get_json()
        for k, v in data_request.items():
            if k != 'id' and k != 'created_at' and k != 'updated_at':
                setattr(amenity, k, v)
                storage.save()
        return jsonify(amenity.to_dict()), 201
    else:
        abort(404)
>>>>>>> master
