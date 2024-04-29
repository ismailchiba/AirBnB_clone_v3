#!/usr/bin/python3

"""
View for Amenity objects that handles all default RESTFul API actions
"""

from flask import jsonify, abort, request
from api.v1.views import app_views, storage
from models.amenity import Amenity


@app_views.route("/amenities", methods=["GET"], strict_slashes=False)
def amenity_get_all():
    """
    Retrieving all Amenity objects

    Return: json of all states
    """

    amenity_list = []
    amenity_object = storage.all("Amenity")

    for obj in amenity_object.values():
        amenity_list.append(obj.to_json())

    return jsonify(amenity_list)


@app_views.route("/amenities", methods=["POST"], strict_slashes=False)
def amenity_create():
    """
    Creating route for amenity

    Return: Newly created amenity obj
    """

    amenity_json = request.get_json(silent=True)
    if amenity_json is None:
        abort(400, 'Not a JSON')
    if "name" not in amenity_json:
        abort(400, 'Missing name')

    new_amenity = Amenity(**amenity_json)
    new_amenity.save()
    response = jsonify(new_amenity.to_json())
    response.status_code = 201

    return response


@app_views.route("/amenities/<amenity_id>",  methods=["GET"],
                 strict_slashes=False)
def amenity_by_id(amenity_id):
    """
    Getting a specific Amenity object by ID
        :amenity_id: amenity object ID

    Return: state obj with the specified ID or error
    """

    fetched_obj = storage.get("Amenity", str(amenity_id))

    if fetched_obj is None:
        abort(404)

    return jsonify(fetched_obj.to_json())


@app_views.route("/amenities/<amenity_id>",  methods=["PUT"],
                 strict_slashes=False)
def amenity_put(amenity_id):
    """
    Updating specific Amenity object by ID
        :amenity_id: amenity object ID

    Return: Amenity object and 200 on success, or 400 or 404 on failure
    """

    amenity_json = request.get_json(silent=True)
    if amenity_json is None:
        abort(400, 'Not a JSON')
    fetched_obj = storage.get("Amenity", str(amenity_id))
    if fetched_obj is None:
        abort(404)
    for key, val in amenity_json.items():
        if key not in ["id", "created_at", "updated_at"]:
            setattr(fetched_obj, key, val)
    fetched_obj.save()
    return jsonify(fetched_obj.to_json())


@app_views.route("/amenities/<amenity_id>",  methods=["DELETE"],
                 strict_slashes=False)
def amenity_delete_by_id(amenity_id):
    """
    Removes Amenity by ID
        :amenity_id: Amenity object id

    Return: Empty dictionary with 200 or 404 if not found
    """

    fetched_obj = storage.get("Amenity", str(amenity_id))

    if fetched_obj is None:
        abort(404)

    storage.delete(fetched_obj)
    storage.save()

    return jsonify({})
