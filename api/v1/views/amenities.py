#!/usr/bin/python3
from api.v1.views import app_views
from flask import jsonify, abort, request
from models.base_model import BaseModel
from models.amenity import Amenity
from models import storage


""" amenities objects view methods, GET/POST/PUT/DELETE request methods"""


@app_views.route("/amenities/")
@app_views.route("/amenities")
def get_amenities():
    """ return llist of amenities"""

    amenities_dict = []
    for amenity in storage.all(Amenity).values():
        amenities_dict.append(amenity.to_dict())
    return jsonify(amenities_dict), 200


@app_views.route("/amenities/<amenity_id>")
@app_views.route("/amenities/<amenity_id>/")
def get_amenity(amenity_id):
    """ get specific amenity"""

    for amenity in storage.all(Amenity).values():
        if amenity.id == amenity_id:
            return jsonify(amenity.to_dict()), 200
    abort(404)


@app_views.route("/amenities/<amenity_id>", methods=['DELETE'])
@app_views.route("/amenities/<amenity_id>/", methods=['DELETE'])
def delete_amenity(amenity_id):
    """ delete amenity"""

    for amenity in storage.all(Amenity).values():
        if amenity.id == amenity_id:
            storage.delete(amenity)
            storage.save()
            return jsonify({}), 200

    abort(404)


@app_views.route("/amenities", methods=['POST'])
@app_views.route("/amenities/", methods=['POST'])
def create_amenity():
    """ create amenity object"""

    create_info = request.get_json()
    if create_info is None:
        abort(400, "NOT a JSON")
    if "name" not in create_info.keys():
        abort(400, "Missing name")

    new_amenity = Amenity(**create_info)
    storage.new(new_amenity)
    storage.save()
    amenity_dict = new_amenity.to_dict()
    return jsonify(amenity_dict), 201


@app_views.route("/amenities/<amenity_id>", methods=["PUT"])
@app_views.route("/amenities/<amenity_id>/", methods=["PUT"])
def amenity_update(amenity_id):
    """ update amenity """

    skip_keys = ["id", "created_at", "updated_at"]
    for amenity in storage.all(Amenity).values():
        if amenity.id == amenity_id:
            amenity_dict = amenity.to_dict()
            storage.delete(amenity)
            storage.save()
            update_info = request.get_json()
            if update_info is None:
                abort(400, "Not a JSON")
            for key, value in update_info.items():
                if key not in skip_keys:
                    amenity_dict[key] = value
            updated_amenity = Amenity(**amenity_dict)
            storage.new(updated_amenity)
            storage.save()
            return jsonify(amenity_dict), 200
    abort(404)
