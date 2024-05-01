#!/usr/bin/python3
"""
route for handling Amenity objects and operations
"""
from flask import jsonify, abort, request, make_response
from api.v1.views import app_views, storage
from models.amenity import Amenity
from werkzeug.exceptions import BadRequest


@app_views.route("/amenities", methods=["GET"], strict_slashes=False)
def get_all_amenities():
    """
    Retrieve all Amenity objects.

    Returns:
        json: A JSON-formatted list of all Amenity objects.
    """

    amenities_lst = []
    amenities = storage.all(Amenity)
    for obj in amenities.values():
        amenities_lst.append(obj.to_json())

    return jsonify(amenities_lst)


@app_views.route(
    "/amenities/<amenity_id>", methods=["GET"], strict_slashes=False
)
def get_amenity(amenity_id):
    """
    Retrieve a specific Amenity object by its ID.

    Args:
        amenity_id (str): The unique identifier of the Amenity object.

    Returns:
        json: A JSON-formatted representation of the Amenity
        object with the specified ID, or an error message if not found.
    """
    amenity = storage.get(Amenity, str(amenity_id))
    if not amenity:
        abort(404)
    return jsonify(amenity.to_dict())


@app_views.route(
    "/amenities/<amenity_id>", methods=["DELETE"], strict_slashes=False
)
def delete_amenity(amenity_id):
    """
    Delete an Amenity object by its ID.

    This function retrieves an Amenity object from the database using the
    provided ID. If the object exists,
    it is deleted and the changes
    are saved to the database.
    It returns an empty JSON response to indicate successful deletion.

    Parameters:
    - amenity_id (str): The unique identifier
    of the Amenity object to be deleted.

    Returns:
    - json: An empty JSON object,
    signifying the successful deletion of the Amenity object.
    """
    amenity = storage.get(Amenity, str(amenity_id))
    if not amenity:
        abort(404)
    storage.delete(amenity)
    storage.save()
    return jsonify({})


@app_views.route("/amenities", methods=["POST"], strict_slashes=False)
def create_amenity():
    """
    Create a new Amenity object.

    Returns:
        json: A JSON-formatted representation
        of the newly created Amenity object.
    """
    try:
        data = request.get_json(silent=True)
        if "name" not in data:
            abort(400, "Missing name")
    except BadRequest:
        abort(400, "Not a JSON")
    new_amenity = Amenity(**data)
    new_amenity.save()
    res = jsonify(new_amenity.to_dict())
    return make_response(res, 201)


@app_views.route(
    "/amenities/<amenity_id>", methods=["PUT"], strict_slashes=False
)
def update_amenity(amenity_id):
    """
    Update an Amenity object identified by its unique ID.

    This function locates an Amenity object in the database
    using its ID and applies the pending updates.
    It returns the updated Amenity object along with
    the HTTP status code indicating the outcome of the operation.

    Parameters:
    - amenity_id (int): The unique identifier of the
    Amenity object to be updated.

    Returns:
    - response: A response object containing the updated
    Amenity object and the HTTP status code.
    """
    amenity = storage.get(Amenity, str(amenity_id))
    if not amenity:
        abort(404)
    try:
        data = request.get_json(silent=True)
    except BadRequest:
        abort(400, "Not a JSON")
    ignore_keys = ["id", "created_at", "updated_at"]
    for key, val in data.items():
        if key not in ignore_keys:
            setattr(amenity, key, val)
    amenity.save()
    res = jsonify(amenity.to_dict())
    return make_response(res, 200)
