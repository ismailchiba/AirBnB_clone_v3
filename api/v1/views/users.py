#!/usr/bin/python3
"""
route for handling User objects and operations
"""
from flask import jsonify, abort, request
from api.v1.views import app_views, storage
from models.user import User


@app_views.route("/users", methods=["GET"], strict_slashes=False)
def user_get_all():
    """
    retrieves all User objects
    :return: json of all users
    """
    user_list = []
    user_obj = storage.all("User")
    for obj in user_obj.values():
        user_list.append(obj.to_json())

    return jsonify(user_list)


@app_views.route("/users", methods=["POST"], strict_slashes=False)
def user_create():
    """
    create user route
    :return: newly created user obj
    """
    user_json = request.get_json(silent=True)
    if user_json is None:
        abort(400, 'Not a JSON')
    if "email" not in user_json:
        abort(400, 'Missing email')
    if "password" not in user_json:
        abort(400, 'Missing password')

    new_user = User(**user_json)
    new_user.save()
    resp = jsonify(new_user.to_json())
    resp.status_code = 201

    return resp


@app_views.route("/users/<user_id>",  methods=["GET"], strict_slashes=False)
def user_by_id(user_id):
    """
    gets a specific User object by ID
    :param user_id: user object id
    :return: user obj with the specified id or error
    """

    fetched_obj = storage.get("User", str(user_id))

    if fetched_obj is None:
        abort(404)

    return jsonify(fetched_obj.to_json())


@app_views.route("/users/<user_id>",  methods=["PUT"], strict_slashes=False)
def user_put(user_id):
    """
    updates specific User object by ID
    :param user_id: user object ID
    :return: user object and 200 on success, or 400 or 404 on failure
    """
    user_json = request.get_json(silent=True)

    if user_json is None:
        abort(400, 'Not a JSON')

    fetched_obj = storage.get("User", str(user_id))

    if fetched_obj is None:
        abort(404)

    for key, val in user_json.items():
        if key not in ["id", "created_at", "updated_at", "email"]:
            setattr(fetched_obj, key, val)

    fetched_obj.save()

    return jsonify(fetched_obj.to_json())


@app_views.route("/users/<user_id>",  methods=["DELETE"], strict_slashes=False)
def user_delete_by_id(user_id):
    """
    deletes User by id
    :param user_id: user object id
    :return: empty dict with 200 or 404 if not found
    """

    fetched_obj = storage.get("User", str(user_id))

    if fetched_obj is None:
        abort(404)

    storage.delete(fetched_obj)
    storage.save()

    return jsonify({})


# #!/usr/bin/python3
# from flask import abort, jsonify, make_response, request
# from api.v1.views import app_views
# from models import storage
# from models.user import User


# @app_views.route('/users', methods=['GET'], strict_slashes=False)
# def retr_users():
#     """Retrieves the list of all User objects."""
#     users = storage.all(User)
#     user_list = [user.to_dict() for user in users.values()]
#     return jsonify(user_list), 200


# @app_views.route('/users/<user_id>', methods=['GET'], strict_slashes=False)
# def get_user(user_id):
#     """Retrieves a User object."""
#     user = storage.get(User, user_id)
#     if user is None:
#         abort(404)
#     return jsonify(user.to_dict())


# @app_views.route('/users/<user_id>',
# methods=['DELETE'], strict_slashes=False)
# def delete_user(user_id):
#     """Deletes a User object."""
#     user = storage.get(User, user_id)
#     if user is None:
#         abort(404)
#     user.delete()
#     storage.save()
#     return jsonify({}), 200


# @app_views.route('/users', methods=['POST'], strict_slashes=False)
# def create_user():
#     """Creates a User."""
#     body_request = request.get_json()
#     if not body_request:
#         return make_response("Not a JSON", 400)
#     if not body_request.get("email"):
#         return make_response("Missing email", 400)
#     if not body_request.get("password"):
#         return make_response("Missing password", 400)

#     user = User(**body_request)
#     user.save()

#     return make_response(jsonify(user.to_dict()), 201)


# @app_views.route('/users/<user_id>', methods=['PUT'], strict_slashes=False)
# def update_user(user_id):
#     """Updates a User object."""
#     user = storage.get(User, user_id)
#     if user is None:
#         abort(404)
#     user_json = request.get_json()
#     if not user_json:
#         return make_response(jsonify({'error': 'Not a JSON'}), 400)
#     for key, value in user_json.items():
#         if key not in ['id', 'created_at', 'updated_at', 'email']:
#             setattr(user, key, value)
#     user.save()
#     return jsonify(user.to_dict()), 200
