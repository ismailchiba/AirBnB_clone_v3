#!/usr/bin/python3

"""
View for the link between Place objects and Amenity
objects that handles all default RESTFul API actions
"""

from flask import jsonify, abort
from os import getenv

from api.v1.views import app_views, storage


@app_views.route("/places/<place_id>/amenities",
                 methods=["GET"],
                 strict_slashes=False)
def amenity_by_place(place_id):
    """
    Fetches all amenities of a place
        :place_id: amenity ID

    Return: All of the amenities
    """

    fetched_object = storage.get("Place", str(place_id))

    all_amenities = []

    if fetched_object is None:
        abort(404)

    for obj in fetched_object.amenities:
        all_amenities.append(obj.to_json())

    return jsonify(all_amenities)


@app_views.route("/places/<place_id>/amenities/<amenity_id>",
                 methods=["DELETE"],
                 strict_slashes=False)
def unlink_amenity_from_place(place_id, amenity_id):
    """
    Unlinking an amenity from a place
        :place_id: place ID
        :amenity_id: amenity ID

    Return: Empty dictionary or error
    """

    if not storage.get("Place", str(place_id)):
        abort(404)
    if not storage.get("Amenity", str(amenity_id)):
        abort(404)

    fetched_object = storage.get("Place", place_id)
    found = 0

    for obj in fetched_object.amenities:
        if str(obj.id) == amenity_id:
            if getenv("HBNB_TYPE_STORAGE") == "db":
                fetched_object.amenities.remove(obj)
            else:
                fetched_object.amenity_ids.remove(obj.id)
            fetched_object.save()
            found = 1
            break

    if found == 0:
        abort(404)
    else:
        response = jsonify({})
        response.status_code = 201
        return response


@app_views.route("/places/<place_id>/amenities/<amenity_id>",
                 methods=["POST"],
                 strict_slashes=False)
def link_amenity_to_place(place_id, amenity_id):
    """
    Linking an amenity to a place
        :place_id: place ID
        :amenity_id: amenity ID

    Return: Amenity obj added or error
    """

    fetched_object = storage.get("Place", str(place_id))
    amenity_object = storage.get("Amenity", str(amenity_id))
    found_amenity = None

    if not fetched_object or not amenity_object:
        abort(404)

    for obj in fetched_object.amenities:
        if str(obj.id) == amenity_id:
            found_amenity = obj
            break

    if found_amenity is not None:
        return jsonify(found_amenity.to_json())

    if getenv("HBNB_TYPE_STORAGE") == "db":
        fetched_object.amenities.append(amenity_object)
    else:
        fetched_object.amenities = amenity_object

    fetched_object.save()

    response = jsonify(amenity_object.to_json())
    response.status_code = 201

    return response
