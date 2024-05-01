#!/usr/bin/python3
"""
route for handling place and amenities linking
"""
from flask import jsonify, abort, make_response
from os import getenv
from models.amenity import Amenity
from models.place import Place
from api.v1.views import app_views, storage


@app_views.route(
    "/places/<place_id>/amenities", methods=["GET"], strict_slashes=False
)
def amenity_by_place(place_id):
    """
    Retrieve all amenities associated with a specific place by its unique ID.

    This function queries the database for all amenities linked to
    the given place ID. It returns a list of amenities,
    providing a comprehensive view of what the place has to offer.

    Parameters:
    - place_id (int or str):
    The unique identifier of the place whose amenities are to be retrieved.

    Returns:
    - list: A list of all amenities associated with the specified place.
    """
    place = storage.get(Place, str(place_id))
    if not place:
        abort(404)
    amenities_lst = []
    for amenity in place.amenities:
        amenities_lst.append(amenity.to_dict())
    return jsonify(amenities_lst)


@app_views.route(
    "/places/<place_id>/amenities/<amenity_id>",
    methods=["DELETE"],
    strict_slashes=False,
)
def unlink_amenity(place_id, amenity_id):
    """
    Unlink an amenity from a specific place by their unique IDs.

    This function removes the association between a
    place and an amenity in the database. If the operation is successful,
    it returns an empty dictionary to signify that the amenity has been
    successfully unlinked from the place.
    If the operation fails, an error message is returned,
    indicating the reason for the failure.

    Parameters:
    - place_id (int or str): The unique identifier of the place.
    - amenity_id (int or str):
        The unique identifier of the amenity to be unlinked.

    Returns:
    - dict: An empty dictionary if the unlinking is successful.
    - error: An error message if the unlinking operation fails.
    """
    place = storage.get(Place, place_id)
    amenity = storage.get(Amenity, str(amenity_id))
    print(place)
    if not place or not amenity:
        abort(404)

    if getenv("HBNB_TYPE_STORAGE") == "db":
        if amenity in place.amenities:
            place.amenities.remove(amenity)
        else:
            abort(404)
    else:
        if amenity.id in place.amenity_ids:
            place.amenity_ids.remove(amenity.id)
        else:
            abort(404)
    place.save()
    return make_response(jsonify({}), 200)


@app_views.route(
    "/places/<place_id>/amenities/<amenity_id>",
    methods=["POST"],
    strict_slashes=False,
)
def link_amenity_to_place(place_id, amenity_id):
    """
    Link an amenity to a specific place using their unique IDs.

    This function establishes a relationship between a placeand an amenity
    in the database. If the linking is successful,
    it returns the Amenity object that was added to the place.
    If the operation fails, an error message is returned,
    indicating the reason for the failure.

    Parameters:
    - place_id (int or str): The unique identifier of the place.
    - amenity_id (int or str):
        The unique identifier of the amenity to be linked.

    Returns:
    - Amenity: The Amenity object that was linked to the
    place if the operation is successful.
    - error: An error message if the linking operation fails.
    """
    place = storage.get(Place, str(place_id))
    amenity = storage.get(Amenity, str(amenity_id))
    if not place or not amenity:
        abort(404)
    if getenv("HBNB_TYPE_STORAGE") == "db":
        if amenity in place.amenities:
            return make_response(jsonify(amenity.to_dict()), 200)
        else:
            place.amenities.append(amenity)
    else:
        if amenity.id in place.amenity_ids:
            return make_response(jsonify(amenity.to_dict()), 200)
        else:
            place.amenity_ids.append(amenity.id)
    place.save()
    res = jsonify(amenity.to_dict())
    return make_response(res, 201)
