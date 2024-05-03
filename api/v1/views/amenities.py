#!/usr/bin/python3
""" RESTFul API - State """

from api.v1.views import app_views
from flask import Flask
from models import storage
from models.amenity import Amenity
from flask import jsonify, request, abort


@app_views.route('/amenities/', methods=['GET'], strict_slashes=False)
def retrieve_list_all_amenities():
    """ Retrieves the list of all Amenity objects: GET /api/v1/amenities """
    if request.method == 'GET':
        list_all_storage = []
        for am in storage.all(Amenity).values():
            list_all_storage.append(am.to_dict())
        return jsonify(list_all_storage)


@app_views.route('/amenities/<amenity_id>', methods=['GET'],
                 strict_slashes=False)
def retrieve_one_amenity(amenity_id):
    """ Retrieves a Amenity object: GET /api/v1/states/<state_id> """
    if request.method == 'GET':
        if storage.get(Amenity, amenity_id) is not None:
            return jsonify(storage.get(Amenity, amenity_id).to_dict())
        abort(404)


@app_views.route('/amenities/<amenity_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_one_amenity(amenity_id):
    """ Deletes a State object:: DELETE /api/v1/states/<state_id> """
    if request.method == 'DELETE':
        if storage.get(Amenity, amenity_id) is not None:
            storage.delete(storage.get(Amenity, amenity_id))
            storage.save()
            return jsonify({}), 200
        abort(404)


@app_views.route('/amenities/', methods=['POST'], strict_slashes=False)
def create_new_amenity():
    """ Creates a State: POST /api/v1/states """
    if request.method == 'POST':
        req_type = request.headers.get('Content-Type')
        if req_type != 'application/json':
            return jsonify('Not a JSON'), 400
        dict_req_name = request.get_json()
        if 'name' not in dict_req_name:
            return jsonify('Missing name'), 400
        new_obj_Amenity = Amenity(**dict_req_name)
        new_obj_Amenity.save()
        return jsonify(new_obj_Amenity.to_dict()), 201


@app_views.route('/amenities/<amenity_id>', methods=['PUT'],
                 strict_slashes=False)
def update_amenity(amenity_id):
    """ Updates a State object: PUT /api/v1/states/<state_id> """
    if request.method == 'PUT':
        req_type = request.headers.get('Content-Type')
        if req_type != 'application/json':
            return jsonify('Not a JSON'), 400
        dict_req = request.get_json()
        if storage.get(Amenity, amenity_id) is not None:
            if 'name' in dict_req:
                storage.get(Amenity, amenity_id).name = dict_req['name']
                storage.get(Amenity, amenity_id).save()
                return jsonify(storage.get(Amenity, amenity_id).to_dict()), 200
        abort(404)
