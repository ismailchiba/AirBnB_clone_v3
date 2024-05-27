#!/usr/bin/python3
"""
handler for Amenity objects and operations routes
"""
from flask import jsonify, abort, request
from models.amenity import Amenity
from api.v1.views import app_views, storage


@app_views.route("/amenities", methods=["GET"], strict_slashes=False)
def amenity_get_all():
    """
    retrieves all Amenity objs
    """
    amenities_list = []
    amenities_object = storage.all("Amenity")
    for obj in amenities_object.values():
        amenities_list.append(obj.to_json())

    return jsonify(amenities_list)


@app_views.route("/amenities", methods=["POST"], strict_slashes=False)
def create_amenity():
    """
    create an amenity route
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
    gets a specific Amenity object by ID
    """

    fetched_object = storage.get("Amenity", str(amenity_id))

    if fetched_object is None:
        abort(404)

    return jsonify(fetched_object.to_json())


@app_views.route("/amenities/<amenity_id>",  methods=["PUT"],
                 strict_slashes=False)
def amenityUpdate_by_id(amenity_id):
    """
    updates specific Amenity object by ID
    """
    amenity_json = request.get_json(silent=True)
    if amenity_json is None:
        abort(400, 'Not a JSON')
    fetched_object = storage.get("Amenity", str(amenity_id))
    if fetched_object is None:
        abort(404)
    for key, value in amenity_json.items():
        if key not in ["id", "created_at", "updated_at"]:
            setattr(fetched_object, key, value)
    fetched_object.save()
    return jsonify(fetched_object.to_json())


@app_views.route("/amenities/<amenity_id>",  methods=["DELETE"],
                 strict_slashes=False)
def amenity_delete_by_id(amenity_id):
    """
    deletes Amenity by id
    """

    fetched_object = storage.get("Amenity", str(amenity_id))

    if fetched_object is None:
        abort(404)

    storage.delete(fetched_object)
    storage.save()

    return jsonify({})
