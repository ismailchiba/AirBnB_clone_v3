#!/usr/bin/python3
"""REST API routes for Amenity objects"""


from api.v1.views import app_views, jsonify
from models.amenity import Amenity
from models import storage
from flask import abort, make_response, request


# GET Requests

@app_views.route("/amenities", methods=["GET"], strict_slashes=False)
def get_amenities():
    """Retrieves the list of all Amenity objects"""

    list_objs = []
    amenities_objs = storage.all(Amenity)

    for obj in amenities_objs.values():
        list_objs.append(obj.to_dict())
    return jsonify(list_objs)


@app_views.route("/amenities/<amenity_id>", methods=["GET"],
                 strict_slashes=False)
def get_amenity(amenity_id):
    """Retrieves a Amenity object by its ID"""
    amenity_obj = storage.get(Amenity, amenity_id)

    if amenity_obj is None:
        abort(404)
    else:
        return jsonify(amenity_obj.to_dict())


@app_views.route("/amenities/<amenity_id>", methods=["DELETE"],
                 strict_slashes=False)
def delete_amenity(amenity_id):
    """Deletes a Amenity object by its ID"""
    amenity_obj = storage.get(Amenity, amenity_id)

    if amenity_obj is None:
        abort(404)

    storage.delete(amenity_obj)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route("/amenities", methods=["POST"], strict_slashes=False)
def post_amenity():
    """Create a new Amenity object"""
    if not request.get_json():
        abort(400, description="Not a JSON")
    if "name" not in request.get_json():
        abort(400, description="Missing name")

    data = request.get_json()
    new_amenity = Amenity(**data)
    new_amenity.save()

    return make_response(jsonify(new_amenity.to_dict()), 201)


@app_views.route("/amenities/<amenity_id>", methods=["PUT"],
                 strict_slashes=False)
def update_amenity(amenity_id):
    """Updates an existing Amenity object"""

    amenity_obj = storage.get(Amenity, amenity_id)

    if amenity_obj is None:
        abort(404)
    if not request.get_json():
        abort(400, description="Not a JSON")

    data = request.get_json()
    ignored_attrs = ["id", "created_at", "updated_at"]
    for key, value in data.items():
        if key not in ignored_attrs:
            setattr(amenity_obj, key, value)

    storage.save()
    return make_response(jsonify(amenity_obj.to_dict()), 200)
