# api/v1/views/places.py
from flask import jsonify, request, abort
from models import storage
from api.v1.views import app_views
from models.city import City
from models.place import Place
from models.user import User

@app_views.route('/cities/<city_id>/places', methods=['GET'])
def get_city_places(city_id):
    """
    Retrieve all places of a city
    """
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    return jsonify([place.to_dict() for place in city.places])

@app_views.route('/places/<place_id>', methods=['GET'])
def get_place(place_id):
    """
    Retrieve a place by id
    """
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    return jsonify(place.to_dict())

@app_views.route('/places/<place_id>', methods=['DELETE'])
def delete_place(place_id):
    """
    Delete a place by id
    """
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    storage.delete(place)
    storage.save()
    return jsonify({}), 200

@app_views.route('/cities/<city_id>/places', methods=['POST'])
def create_place(city_id):
    """
    Create a new place
    """
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    if not request.json:
        abort(400, "Not a JSON")
    if 'user_id' not in request.json:
        abort(400, "Missing user_id")
    user_id = request.json['user_id']
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    if 'name' not in request.json:
        abort(400, "Missing name")
    data = request.json
    data['city_id'] = city_id
    new_place = Place(**data)
    new_place.save()
    return jsonify(new_place.to_dict()), 201

@app_views.route('/places/<place_id>', methods=['PUT'])
def update_place(place_id):
    """
    Update a place by id
    """
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    if not request.json:
        abort(400, "Not a JSON")
    data = request.json
    for key, value in data.items():
        if key not in ['id', 'user_id', 'city_id', 'created_at', 'updated_at']:
            setattr(place, key, value)
    place.save()
    return jsonify(place.to_dict()), 200

