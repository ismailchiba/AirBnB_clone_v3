from flask import jsonify, abort, request
from api.v1.views import app_views, storage
from models.place import Place

@app_views.route("/cities/<city_id>/places", methods=["GET"], strict_slashes=False)
def places_by_city(city_id):
    """
    Retrieves all Place objects by city.
    :return: JSON response containing all Places in the specified city.
    """
    place_list = []
    city_obj = storage.get("City", str(city_id))
    if city_obj is None:
        abort(404, "City not found")
    for obj in city_obj.places:
        place_list.append(obj.to_json())
    return jsonify(place_list)

@app_views.route("/cities/<city_id>/places", methods=["POST"], strict_slashes=False)
def place_create(city_id):
    """
    Creates a new place in the specified city.
    :return: JSON response containing the newly created Place object.
    """
    place_json = request.get_json(silent=True)
    if place_json is None:
        abort(400, 'Invalid JSON')
    required_fields = ["name", "user_id"]
    for field in required_fields:
        if field not in place_json:
            abort(400, f'Missing {field}')
    city_obj = storage.get("City", city_id)
    if city_obj is None:
        abort(404, "City not found")
    user_obj = storage.get("User", place_json["user_id"])
    if user_obj is None:
        abort(404, "User not found")
    place_json["city_id"] = city_id
    new_place = Place(**place_json)
    new_place.save()
    return jsonify(new_place.to_json()), 201

@app_views.route("/places/<place_id>", methods=["GET"], strict_slashes=False)
def place_by_id(place_id):
    """
    Retrieves a specific Place object by ID.
    :param place_id: Place object ID.
    :return: JSON response containing the Place object with the specified ID.
    """
    fetched_obj = storage.get("Place", str(place_id))
    if fetched_obj is None:
        abort(404, "Place not found")
    return jsonify(fetched_obj.to_json())

@app_views.route("/places/<place_id>", methods=["PUT"], strict_slashes=False)
def place_put(place_id):
    """
    Updates a specific Place object by ID.
    :param place_id: Place object ID.
    :return: JSON response containing the updated Place object.
    """
    place_json = request.get_json(silent=True)
    if place_json is None:
        abort(400, 'Invalid JSON')
    fetched_obj = storage.get("Place", str(place_id))
    if fetched_obj is None:
        abort(404, "Place not found")
    for key, val in place_json.items():
        if key not in ["id", "created_at", "updated_at", "user_id", "city_id"]:
            setattr(fetched_obj, key, val)
    fetched_obj.save()
    return jsonify(fetched_obj.to_json())

@app_views.route("/places/<place_id>", methods=["DELETE"], strict_slashes=False)
def place_delete_by_id(place_id):
    """
    Deletes a Place by ID.
    :param place_id: Place object ID.
    :return: Empty JSON response with status code 200 if successful, or 404 if not found.
    """
    fetched_obj = storage.get("Place", str(place_id))
    if fetched_obj is None:
        abort(404, "Place not found")
    storage.delete(fetched_obj)
    storage.save()
    return jsonify({}), 200
