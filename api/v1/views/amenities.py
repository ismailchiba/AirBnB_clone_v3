#!/usr/bin/python3

"""Interact with the Amenity model"""

from flask import Flask as F, abort, jsonify, request as RQ
from api.v1.views import app_views as AV
from models import storage
from models.amenity import Amenity
from models.base_model import BaseModel as BM


amenities = F(__name__)


@AV.route('/amenities', methods=['GET', 'POST'])
def get_or_create_amenities():
    """Get all amenities / Create a new amenity w no Id"""
    Amenitys = storage.all('Amenity')
    if Amenitys is None:
        abort(404, 'Not found')

    if RQ.method == 'GET':
        response = [amenity.to_dict() for amenity in Amenitys.values()]
        status = 200

    if RQ.method == 'POST':
        RQ_json = RQ.get_json()
        if RQ_json is None:
            abort(400, 'Not a JSON')
        if RQ_json.get('name') is None:
            abort(400, 'Missing name')

        new_amenity = Amenity(**RQ_json)
        new_amenity.save()
        response = new_amenity.to_dict()
        status = 201
    return jsonify(response), status


@AV.route('/amenities/<amenity_id>', methods=['GET', 'PUT', 'DELETE'])
def get_del_put_amenity(amenity_id=None):
    """Get, delete or update a Amenity object w a given identifier"""
    response = {}
    amenity = storage.get('Amenity', amenity_id)
    if amenity is None:
        abort(404, "Not found")

    if RQ.method == 'GET':
        response = amenity.to_dict()
        status = 200

    if RQ.method == 'PUT':
        RQ_json = RQ.get_json()
        if RQ_json is None:
            abort(400, 'Not a JSON')

        amenity = Amenity.db_update(RQ_json)
        amenity.save()   # type: ignore
        response = amenity.to_dict()   # type: ignore
        status = 200

    if RQ.method == 'DELETE':
        amenity.delete()   # type: ignore
        del amenity
        status = 200
    return jsonify(response), status
