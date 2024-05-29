from api.v1.views import app_views
from flask import jsonify, abort, request
from models.base_model import BaseModel
from models.amenity import Amenity
from models import storage
import json

@app_views.route("/amenities/")
def get_amenities():
    """ return llist of amenities"""

    amenities_dict = []
    for value in storage.all(Amenity).values():
        amenities_dict.append(value.to_dict())
    return json.dumps(amenities_dict, indent=2) + '\n'


@app_views.route("/amenities/<amenity_id>")
def get_amenity(amenity_id):
    """ get specific amenity"""

    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    return json.dumps(amenity.to_dict(), indent=2) + '\n'


@app_views.route("/amenities/<amenity_id>", methods=['DELETE'])
def delete_amenity(amenity_id):
    """ delete amenity provided ID"""

    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    storage.delete(amenity)
    storage.save()
    return json.dumps({}, indent=2) + '\n'


@app_views.route("/amenities", methods=['POST'])
def create_amenity():
    """ create amenity object"""

    obj_dict = request.get_json()
    if obj_dict is None:
        abort(400, "NOT a JSON")
    if "name" not in obj_dict.keys():
        abort(400, "Missing name")

    obj = Amenity(**obj_dict)
    storage.new(obj)
    storage.save()
    x = obj.to_dict()
    return json.dumps(x, indent=2) + '\n', 201

@app_views.route("/amenities/<amenity_id>", methods=["PUT"])
def amenity_update(amenity_id):
    """ update amenity """

    obj = storage.all(Amenity)
    skip_keys = ["id", "created_at", "updated_at"]
    available = False
    for key in obj.keys():
        if key.split('.')[-1] == amenity_id:
            available = True
            amenity = obj[key]
            obj_dict = amenity.to_dict()
            break

    if available is False:
        abort(404)
    up_dict = request.get_json()
    if up_dict is None:
        abort(400, "Not a JSON")
    storage.delete(amenity)
    storage.save()
    for ky, value in up_dict.items():
        if ky not in skip_keys:
            obj_dict[ky] = value
    obj = Amenity(**obj_dict)
    storage.new(obj)
    storage.save()
    return json.dumps(obj.to_dict(), indent=2) + '\n', 200 

