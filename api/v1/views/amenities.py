#!/usr/bin/python3
"""
This module defines Flask routes to provide API endpoints
for Amenity objects.
"""
from flask import abort, jsonify, make_response, request

from api.v1.views import app_views
from models import storage
from models.amenity import Amenity

api_route = "/amenities/<string:amenity_id>"


@app_views.route("/amenities", methods=["GET"], strict_slashes=False)
def get_amenities():
    """
    Retrieves the list of all Amenity objects
    """
    amenities_list = []
    amenities_obj = storage.all(Amenity)

    for obj in amenities_obj.values():
        amenities_list.append(obj.to_dict())

    response = jsonify(amenities_list), 200

    return response


@app_views.route("/amenities", methods=["POST"], strict_slashes=False)
def create_amenity():
    """
    Create a new amenity.

    Returns:
        tuple: A tuple containing the JSON representation
        of the new amenity and the HTTP status code 201.
    """
    body = request.get_json(silent=True)

    if not body:
        return make_response(jsonify({"error": "Not a JSON"}), 400)

    if "name" not in body:
        return make_response(jsonify({"error": "Missing name"}), 400)

    new_amenity = Amenity(**body)

    new_amenity.save()

    response = jsonify(new_amenity.to_dict()), 201

    return make_response(response)


@app_views.route(api_route, methods=["GET"], strict_slashes=False)
def get_amenity_by_id(amenity_id):
    """
    Retrieve a specific amenity by its ID.

    Args:
        amenity_id (str): The ID of the amenity to retrieve.

    Returns:
        tuple: A tuple containing the JSON representation of
        the amenity and the HTTP status code.

    Raises:
        404: If the amenity with the specified ID does not exist.
    """
    amenity = storage.get(Amenity, amenity_id)

    if amenity is None:
        abort(404)

    response = jsonify(amenity.to_dict()), 200

    return response


@app_views.route(api_route, methods=["DELETE"], strict_slashes=False)
def delete_amenity(amenity_id):
    """
    Delete a amenity by its ID.

    Args:
        amenity_id (str): The ID of the amenity to delete.

    Returns:
        tuple: An empty dictionary and the HTTP status code 200.

    Raises:
        404: If the amenity with the specified ID does not exist.
    """
    amenity = storage.get(Amenity, amenity_id)

    if amenity is None:
        abort(404)

    storage.delete(amenity)
    storage.save()

    return jsonify({})


@app_views.route(api_route, methods=["PUT"], strict_slashes=False)
def update_amenity(amenity_id):
    """
    Update a amenity by its ID.

    Args:
        amenity_id (str): The ID of the amenity to update.

    Returns:
        tuple: A tuple containing the JSON representation
        of the updated amenity and the HTTP status code 200.

    Raises:
        404: If the amenity with the specified ID does not exist.
    """
    body = request.get_json(silent=True)

    if not body:
        return make_response(jsonify({"error": "Not a JSON"}), 400)

    amenity = storage.get(Amenity, str(amenity_id))

    if amenity is None:
        abort(404)

    for key, value in body.items():
        if key not in ["id", "created_at", "updated_at"]:
            setattr(amenity, key, value)

    storage.save()

    response = jsonify(amenity.to_dict()), 200

    return response
