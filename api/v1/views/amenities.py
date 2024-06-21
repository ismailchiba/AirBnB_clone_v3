#!/usr/bin/python3
""" This module is to handle routes related to the amenities
"""
from flask import Blueprint, abort, request
from werkzeug.exceptions import BadRequest
from models import storage
from models.amenity import Amenity

app_amenities = Blueprint("app_amenities", __name__)


def get_object_by_id(cls, obj_id):
    """ This function is used to retrive a specific object using its id
    """
    for _, obj in storage.all(cls).items():
        if obj.id == obj_id:
            return obj
    return None


@app_amenities.route("/", methods=['GET'])
def retrive_all_amenities():
    """ This function return list of all amenities """
    return [obj.to_dict() for _, obj in storage.all(Amenity).items()]


@app_amenities.route("/<amenity_id>", methods=['GET'])
def retrive_amenity(amenity_id):
    """ This function is used to retrive a specific amenity
        object using its id
    """
    amenity = get_object_by_id(Amenity, amenity_id)
    if not amenity:
        abort(404)
    return amenity.to_dict()


@app_amenities.route("/<amenity_id>", methods=['DELETE'])
def delete_amenity(amenity_id):
    """ This function is used to delete an amenity object when
        the DELETE method is called
    """
    amenity = get_object_by_id(Amenity, amenity_id)
    if not amenity:
        abort(404)
    storage.delete(amenity)
    storage.save()
    return {}, 200


@app_amenities.route("/", methods=['POST'])
def create_amenity():
    """ This function creates a new amenity object
    """
    try:
        request_data = request.get_json()
    except BadRequest:
        abort(400, description="Not a JSON")

    if 'name' not in request_data:
        abort(400, description="Missing name")
    new_amenity = Amenity()
    new_amenity.name = request_data.get('name')
    new_amenity.save()
    return new_amenity.to_dict(), 201


@app_amenities.route("/<amenity_id>", methods=['PUT'])
def update_amenity(amenity_id):
    """ This function updates an existing amenity object
    """
    amenity = get_object_by_id(Amenity, amenity_id)
    if not amenity:
        abort(404)
    try:
        request_data = request.get_json()
    except BadRequest:
        abort(400, description="Not a JSON")

    for key, value in request_data.items():
        if key not in ('id', 'created_at', 'updated_at'):
            setattr(amenity, key, value)
    amenity.save()
    return amenity.to_dict(), 200
