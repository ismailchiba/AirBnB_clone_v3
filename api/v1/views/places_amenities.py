#!/usr/bin/python3
"""
route for handling place and amenities
"""
from flask import jsonify, abort
from os import getenv

from api.v1.views import app_views, storage


@app_views.route("/places/<place_id>/amenities",
                 methods=["GET"],
                 strict_slashes=False)
def amenities_by_place(place_id):
    """
    get all amenities of a place
    """
    fetched_obj = storage.get("Place", str(place_id))

    all_amenities = []

    if fetched_obj is None:
        abort(404)

    for obj in fetched_obj.amenities:
        all_amenities.append(obj.to_json())

    return jsonify(all_amenities)


@app_views.route("/places/<place_id>/amenities/<amenity_id>",
                 methods=["DELETE"],
                 strict_slashes=False)
def unlinkAmenity_from_place(place_id, amenity_id):
    """
    unlinks an amenity in a place
    return: empty dict or error
    """
    if not storage.get("Place", str(place_id)):
        abort(404)
    if not storage.get("Amenity", str(amenity_id)):
        abort(404)

    fetched_obj = storage.get("Place", place_id)
    seen = 0

    for obj in fetched_obj.amenities:
        if str(obj.id) == amenity_id:
            if getenv("HBNB_TYPE_STORAGE") == "db":
                fetched_obj.amenities.remove(obj)
            else:
                fetched_obj.amenity_ids.remove(obj.id)
            fetched_obj.save()
            seen = 1
            break

    if seen == 0:
        abort(404)
    else:
        response = jsonify({})
        response.status_code = 201
        return response


@app_views.route("/places/<place_id>/amenities/<amenity_id>",
                 methods=["POST"],
                 strict_slashes=False)
def linkAmenity_to_place(place_id, amenity_id):
    """
    links a amenity with a place
    return: return Amenity obj added or error
    """

    fetched_object = storage.get("Place", str(place_id))
    amenity_object = storage.get("Amenity", str(amenity_id))
    seen_amenity = None

    if not fetched_object or not amenity_object:
        abort(404)

    for obj in fetched_object.amenities:
        if str(obj.id) == amenity_id:
            seen_amenity = obj
            break

    if seen_amenity is not None:
        return jsonify(seen_amenity.to_json())

    if getenv("HBNB_TYPE_STORAGE") == "db":
        fetched_object.amenities.append(amenity_object)
    else:
        fetched_object.amenities = amenity_object

    fetched_object.save()

    response = jsonify(amenity_object.to_json())
    response.status_code = 201

    return response
