#!/usr/bin/python3
"""handle place and amenities operation"""

from flask import jsonify, abort
from os import getenv
from api.v1.views import app_views, storage


@app_views.route("/places/<place_id>/amenities",methods=["GET"],
                 strict_slashes=False)
def get_amenity_by_place(place_id):
    """get all amenities of a place"""
    amenity_obj = storage.get("Place", str(place_id))
    all_amenities = []
    if amenity_obj is None:
        abort(404)
    for obj in amenity_obj.amenities:
        all_amenities.append(obj.to_json())
    return jsonify(all_amenities)


@app_views.route("/places/<place_id>/amenities/<amenity_id>", methods=["DELETE"],
                 strict_slashes=False)
def unlinked_amenity_place(place_id, amenity_id):
    """unlink amenity from a place"""
    if not storage.get("Place", str(place_id)):
        abort(404)
    if not storage.get("Amenity", str(amenity_id)):
        abort(404)
    amenity_obj = storage.get("Place", place_id)
    found = 0

    for obj in amenity_obj.amenities:
        if str(obj.id) == amenity_id:
            if getenv("HBNB_TYPE_STORAGE") == "db":
                amenity_obj.amenities.remove(obj)
            else:
                amenity_obj.amenity_ids.remove(obj.id)
            amenity_obj.save()
            found = 1
            break
    if found == 0:
        abort(404)
    else:
        resp = jsonify({})
        resp.status_code = 201
        return resp


@app_views.route("/places/<place_id>/amenities/<amenity_id>", methods=["POST"],
                 strict_slashes=False)
def link_amenity_place(place_id, amenity_id):
    """links a amenity with a place"""
    pamenity_obj = storage.get("Place", str(place_id))
    amenity_obj = storage.get("Amenity", str(amenity_id))
    found_amenity = None

    if not pamenity_obj or not amenity_obj:
        abort(404)
    for obj in pamenity_obj.amenities:
        if str(obj.id) == amenity_id:
            found_amenity = obj
            break
    if found_amenity is not None:
        return jsonify(found_amenity.to_json())

    if getenv("HBNB_TYPE_STORAGE") == "db":
        pamenity_obj.amenities.append(amenity_obj)
    else:
        pamenity_obj.amenities = amenity_obj

    pamenity_obj.save()
    resp = jsonify(amenity_obj.to_json())
    resp.status_code = 201
    return resp
