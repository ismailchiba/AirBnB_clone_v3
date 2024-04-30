#!/usr/bin/python3
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
