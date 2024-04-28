#!/usr/bin/python3
"""handle Amenity operations"""

from flask import jsonify, abort, request
from api.v1.views import app_views, storage
from models.amenity import Amenity


@app_views.route("/amenities", methods=["GET"], strict_slashes=False)
def amenity_get_all():
    """
    retrieves all Amenity objects
    :return: json of all states
    """
    am_list = []
    am_obj = storage.all("Amenity")
    for obj in am_obj.values():
        am_list.append(obj.to_json())

    return jsonify(am_list)


@app_views.route("/amenities/<amenity_id>",  methods=["GET"], strict_slashes=False)
def amenity_by_id(amenity_id):
    """get amenity using its specific id"""
    amenity_obj = storage.get("Amenity", str(amenity_id))
    if not amenity_obj:
        abort(404)
    return jsonify(amenity_obj.to_json())


@app_views.route("/amenities", methods=["POST"], strict_slashes=False)
def amenity_create():
    """create a new amenity"""
    amenity_json = request.get_json(silent=True)
    if amenity_json is None:
        abort(400, 'Not a JSON')
    if "name" not in amenity_json:
        abort(400, 'Missing name')

    new_amenitys = Amenity(**amenity_json)
    new_amenitys.save()
    resp = jsonify(new_amenitys.to_json())
    resp.status_code = 201

    return resp


@app_views.route("/amenities/<amenity_id>",  methods=["PUT"], strict_slashes=False)
def amenity_put_id(amenity_id):
    """updates Amenity using its specific ID"""
    amenity_json = request.get_json(silent=True)
    if not amenity_json:
        abort(400, 'Not a JSON')
    amenity_obj = storage.get("Amenity", str(amenity_id))
    if amenity_obj is None:
        abort(404)
    for key, value in amenity_json.items():
        if key not in ["id", "created_at", "updated_at"]:
            setattr(amenity_obj, key, value)
    amenity_obj.save()
    return jsonify(amenity_obj.to_json())


@app_views.route("/amenities/<amenity_id>",  methods=["DELETE"], strict_slashes=False)
def amenity_delete_id(amenity_id):
    """deletes Amenity using its specific id"""
    amenity_obj = storage.get("Amenity", str(amenity_id))
    if amenity_obj is None:
        abort(404)

    storage.delete(amenity_obj)
    storage.save()
    return jsonify({})
