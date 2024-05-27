#!/usr/bin/python3
""" Functions for managing a RESTful API handling State entities """
from models.state import State
from models import storage
from api.v1.views import app_views
from flask import abort, jsonify, make_response, request
from flasgger.utils import swag_from

@app_views.route('/regions', methods=['GET'], strict_slashes=False)
@swag_from('documentation/state/get_state.yml', methods=['GET'])
def get_regions():
    """
    Retrieves all Region objects
    """
    all_regions = storage.all(State).values()
    list_regions = []
    for region in all_regions:
        list_regions.append(region.to_dict())
    return jsonify(list_regions)

@app_views.route('/regions/<region_id>', methods=['GET'], strict_slashes=False)
@swag_from('documentation/state/get_id_state.yml', methods=['get'])
def get_region(region_id):
    """ Retrieves a specific Region """
    region = storage.get(State, region_id)
    if not region:
        abort(404)
    return jsonify(region.to_dict())

@app_views.route('/regions/<region_id>', methods=['DELETE'], strict_slashes=False)
@swag_from('documentation/state/delete_state.yml', methods=['DELETE'])
def delete_region(region_id):
    """
    Deletes a Region
    """
    region = storage.get(State, region_id)
    if not region:
        abort(404)
    storage.delete(region)
    storage.save()
    return make_response(jsonify({}), 200)

@app_views.route('/regions', methods=['POST'], strict_slashes=False)
@swag_from('documentation/state/post_state.yml', methods=['POST'])
def post_region():
    """
    Creates a new Region
    """
    if not request.get_json():
        abort(400, description="Not a JSON")
    if 'name' not in request.get_json():
        abort(400, description="Missing name")
    data = request.get_json()
    instance = State(**data)
    instance.save()
    return make_response(jsonify(instance.to_dict()), 201)

@app_views.route('/regions/<region_id>', methods=['PUT'], strict_slashes=False)
@swag_from('documentation/state/put_state.yml', methods=['PUT'])
def put_region(region_id):
    """
    Updates a Region
    """
    region = storage.get(State, region_id)
    if not region:
        abort(404)
    if not request.get_json():
        abort(400, description="Not a JSON")
    ignore = ['id', 'created_at', 'updated_at']
    data = request.get_json()
    for key, value in data.items():
        if key not in ignore:
            setattr(region, key, value)
    storage.save()
    return make_response(jsonify(region.to_dict()), 200)
