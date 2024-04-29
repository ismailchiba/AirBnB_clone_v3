#!/usr/bin/python3
from api.v1.views import app_views
from flask import abort, jsonify, make_response, request
from models import storage
from models.user import User


@app_views.route('/users', methods=['GET'])
def get_all_user():
    """Get all users from the storage."""
    users = storage.all(User)
    user_list = [value.to_dict() for value in users.values()]
    return make_response(jsonify(user_list), 200)


@app_views.route('/users/<user_id>', methods=['GET'])
def get_user_by_id(user_id):
    """Return user based on a corresponding id."""
    user_by_id = storage.get(User, user_id)
    if not user_by_id:
        abort(404)
    return jsonify(user_by_id.to_dict())


@app_views.route('/users/<user_id>', methods=['DELETE'])
def delete_user(user_id):
    """Deletes a user with specific id."""
    user_by_id = storage.get(User, user_id)
    if not user_by_id:
        abort(404)

    user_by_id.delete()
    storage.save()

    return make_response({}, 200)


@app_views.route('/users', methods=['POST'])
def create_user():
    """Creates new user."""
    body_request = request.get_json()
    if not body_request:
        return make_response("Not a JSON", 400)
    if not body_request.get("email"):
        return make_response("Missing email", 400)
    if not body_request.get("password"):
        return make_response("Missing password", 400)

    user = User(**body_request)
    user.save()

    return make_response(jsonify(user.to_dict()), 201)


@app_views.route('/users/<user_id>', methods=['PUT'])
def update_user(user_id):
    """Updates a state with specific id."""
    user_by_id = storage.get(User, user_id)
    if not user_by_id:
        abort(404)

    body_request = request.get_json()
    if not body_request:
        return make_response("Not a JSON", 400)

    attributes_to_update = ['first_name', 'last_name', 'email', 'password']
    for attribute in attributes_to_update:
        setattr(user_by_id, attribute,
                body_request.get(attribute, getattr(user_by_id, attribute)))
    storage.save()

    return make_response(jsonify(user_by_id.to_dict()), 200)
# @app_views.route('/users', strict_slashes=False, methods=['GET'])
# def get_users():
#     """Retrieves the list of all User objects."""
#     return jsonify([user.to_dict() for user in storage.all(User).values()])


# @app_views.route('/users/<user_id>',
#                  strict_slashes=False, methods=['GET'])
# def get_user(user_id):
#     """Retrieves a User object."""
#     user = storage.get(User, user_id)
#     if user is None:
#         abort(404)
#     return jsonify(user.to_dict())


# @app_views.route('/users/<user_id>',
#                  strict_slashes=False, methods=['DELETE'])
# def delete_user(user_id):
#     """Deletes a User object."""
#     if user_id is None:
#         abort(404)

#     user_id.delete()
#     storage.save()
#     return make_response({}, 200)


# @app_views.route('/users', strict_slashes=False, methods=['POST'])
# def create_user():
#     """Creates a User."""
#     user_json = request.get_json()
#     if user_json is None:
#         return make_response(jsonify({'error': 'Not a JSON'}), 400)
#     if 'email' not in user_json:
#         return make_response(jsonify({'error': 'Missing email'}), 400)
#     if 'password' not in user_json:
#         return make_response(jsonify({'error': 'Missing password'}), 400)
#     user = User(**user_json)
#     user.save()
#     return make_response(jsonify(user.to_dict()), 201)


# @app_views.route('/users/<user_id>',
#                  strict_slashes=False, methods=['PUT'])
# def update_user(user_id):
#     """Updates a User object."""
#     user_by_id = storage.get(User, user_id)
#     if not user_by_id:
#         abort(404)

#     body_request = request.get_json()
#     if not body_request:
#         return make_response("Not a JSON", 400)

#     attributes_to_update = ['first_name', 'last_name', 'email', 'password']
#     for attribute in attributes_to_update:
#         setattr(user_by_id, attribute,
#                 body_request.get(attribute, getattr(user_by_id, attribute)))
#     storage.save()

#     return make_response(jsonify(user_by_id.to_dict()), 200)
