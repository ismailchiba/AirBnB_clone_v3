
m flask import jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.place import Place

@app_views.route("/cities/<city_id>/places", methods=["GET"], strict_slashes=False)
def places_by_city(city_id):
    """Retrieve all Place objects by city."""
    city = storage.get("City", city_id)
    if not city:
        abort(404, "City not found")
    places = [place.to_json() for place in city.places]
    return jsonify(places)

@app_views.route("/cities/<city_id>/places", methods=["POST"], strict_slashes=False)
def place_create(city_id):
    """Create a new place in the specified city."""
    city = storage.get("City", city_id)
    if not city:
        abort(404, "City not found")
    data = request.get_json()
    if not data:
        abort(400, "Invalid JSON")
    if "user_id" not in data:
        abort(400, "Missing user_id")
    user = storage.get("User", data["user_id"])
    if not user:
        abort(404, "User not found")
    if "name" not in data:
        abort(400, "Missing name")
    data["city_id"] = city_id
    place = Place(**data)
    place.save()
    return jsonify(place.to_json()), 201

@app_views.route("/places/<place_id>", methods=["GET"], strict_slashes=False)
def place_by_id(place_id):
    """Retrieve a specific Place object by ID."""
    place = storage.get("Place", place_id)
    if not place:
        abort(404, "Place not found")
    return jsonify(place.to_json())

@app_views.route("/places/<place_id>", methods=["PUT"], strict_slashes=False)
def place_update(place_id):
    """Update a specific Place object by ID."""
    place = storage.get("Place", place_id)
    if not place:
        abort(404, "Place not found")
    data = request.get_json()
    if not data:
        abort(400, "Invalid JSON")
    for key, value in data.items():
        if key not in ["id", "created_at", "updated_at", "user_id", "city_id"]:
            setattr(place, key, value)
    place.save()
    return jsonify(place.to_json())

@app_views.route("/places/<place_id>", methods=["DELETE"], strict_slashes=False)
def place_delete(place_id):
    """Delete a specific Place object by ID."""
    place = storage.get("Place", place_id)
    if not place:
        abort(404, "Place not found")
    storage.delete(place)
    storage.save()
    return jsonify({}), 200

