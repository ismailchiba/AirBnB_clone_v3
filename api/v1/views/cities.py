#!/usr/bin/python3
"""Implement city view"""

from api.v1.views import app_views
from flask import abort, jsonify, make_response, request
from models import storage
from models.city import City
from models.state import State


@app_views.route('/states/<state_id>/cities', methods=['GET'])
def get_cities(state_id):
    """get a list of cities """
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    cities = [obj.to_dict() for obj in state.cities]
    return make_response(jsonify(cities), 200)


@app_views.route('/cities/<city_id>', methods=['GET'])
def get_city(city_id):
    """get city by id"""
    city = storage.get(City, city_id)
    return make_response(jsonify(city.to_dict()),
                         200) if city else abort(404)


@app_views.route('/cities/<city_id>', methods=['DELETE'])
def delete_city(city_id):
    """delete city"""
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    city.delete()
    storage.save()
    return make_response({}, 200)


@app_views.route('states/<state_id>/cities', methods=['POST'])
def create_city(state_id):
    """create a new city"""
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    city = request.get_json()
    if not city:
        return make_response("Not a JSON", 400)
    if not city.get('name'):
        return make_response("Missing name", 400)
    city['state_id'] = state_id
    new_city = City(**city)
    new_city.save()
    return make_response(jsonify(new_city.to_dict()), 201)


@app_views.route('cities/<city_id>', methods=['PUT'])
def update_city(city_id):
    """update a city by id"""
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    req_city = request.get_json()
    if not req_city:
        return make_response("Not a JSON", 400)
    setattr(city, 'name', req_city.get('name'))
    storage.save()
    return make_response(city.to_dict(), 200)


# #!/usr/bin/python3
# from flask import jsonify, abort, request, make_response
# from api.v1.views import app_views
# from models import storage
# from models.city import City
# from models.state import State


# @app_views.route('/states/<state_id>/cities', methods=['GET'])
# def ret_city(state_id):
#     """Retrieves the list of all City objects"""
#     state = storage.get(State, state_id)
#     if not state:
#         abort(404)
#     all_cities = [obj.to_dict() for obj in state.cities]
#     return make_response(jsonify(all_cities), 200)


# @app_views.route('/cities/<city_id>', strict_slashes=False, methods=['GET'])
# def get_city(city_id):
#     """Retrieves a City object"""
#     city = storage.get(City, city_id)
#     if city:
#         return (jsonify(city.to_dict()), 200)
#     else:
#         abort(404)


# @app_views.route('/cities/<city_id>', strict_slashes=False, methods=['DELETE'])
# def delete_city(city_id):
#     """Deletes a City object"""
#     city = storage.get(City, city_id)
#     if city:
#         city.delete()
#         storage.save()
#         return (make_response({}), 200)
#     else:
#         abort(404)


# @app_views.route('/states/<state_id>/cities',
#                  strict_slashes=False, methods=['POST'])
# def create_city(state_id):
#     """Creates a City"""
#     state = storage.get(State, state_id)
#     if not state:
#         abort(404)
#     if not request.get_json():
#         return make_response(jsonify({"error": "Not a JSON"}), 400)
#     if 'name' not in request.get_json():
#         return make_response(jsonify({"error": "Missing name"}), 400)
#     city = City(**request.get_json())
#     city.state_id = state_id
#     city.save()
#     return make_response(jsonify(city.to_dict()), 201)


# @app_views.route('/cities/<city_id>', strict_slashes=False, methods=['PUT'])
# def update_city(city_id):
#     """Updates a City object"""
#     city = storage.get(City, city_id)
#     if not city:
#         abort(404)
#     if not request.get_json():
#         return make_response(jsonify({"error": "Not a JSON"}), 400)
#     for k, v in request.get_json().items():
#         if k not in ['id', 'state_id', 'created_at', 'updated_at']:
#             setattr(city, k, v)
#     city.save()
#     return make_response(jsonify(city.to_dict()), 200)
