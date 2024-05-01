#!/usr/bin/python3
"""
route for handling User objects and operations
"""
from flask import jsonify, abort, request, make_response
from api.v1.views import app_views, storage
from models.user import User
from werkzeug.exceptions import BadRequest


@app_views.route("/users", methods=["GET"], strict_slashes=False)
def get_all():
    """
    Retrieve all User objects from the database.

    This function queries the database for all stored User objects
    and returns them in a JSON-formatted list.
    It is typically used to display all users
    in the system to an administrator or for debugging purposes.

    Returns:
    - json: A JSON-formatted list of all User objects in the database.
    """
    users_lst = []
    users = storage.all(User)
    for obj in users.values():
        users_lst.append(obj.to_dict())

    return jsonify(users_lst)


@app_views.route("/users/<user_id>", methods=["GET"], strict_slashes=False)
def get_user(user_id):
    """
    Retrieve a specific User object by its unique ID.

    This function searches the database for a User object that matches
    the provided ID. If the object is found, it is returned in its entirety.
    If no matching User object is found, an error message
    is generated and returned, indicating that
    the requested object does not exist.

    Parameters:
    - user_id (int or str): The unique
    identifier of the User object to retrieve.

    Returns:
    - user: The User object with the specified ID if found.
    - error: An error message if no User object with the
    """
    user = storage.get(User, str(user_id))
    if not user:
        abort(404)
    return jsonify(user.to_dict())


@app_views.route("/users/<user_id>", methods=["DELETE"], strict_slashes=False)
def delete_user(user_id):
    """
    Delete a User object from the database by its unique ID.

    This function attempts to find and delete a User object
    based on the provided ID.
    If the object is successfully found and deleted,
    it returns an empty dictionary and a 200 HTTP status code,
    indicating a successful
    operation. If the User object cannot be found,
    it returns a 404 HTTP status code to indicate that
    the resource was not found.

    Parameters:
    - user_id (int or str): The unique identifier
    of the User object to be deleted.

    Returns:
    - dict: An empty dictionary if the deletion is successful.
    - int: An HTTP status code of 200 for
    successful deletion or 404 if the User object is not found.
    """
    user = storage.get(User, str(user_id))
    if user is None:
        abort(404)
    storage.delete(user)
    storage.save()

    return make_response(jsonify({}), 200)


@app_views.route("/users", methods=["POST"], strict_slashes=False)
def create_user():
    """
    Create a new User object and store it in the database.

    This function collects the necessary data from
    the request, creates a new User object, and saves it to the database.
    It returns the newly created User object, typically including details
    such as the username, email, and any other relevant user information.

    Returns:
    - user: The newly created User
    object with its attributes populated as per the request data.
    """
    try:
        data = request.get_json(silent=True)
        if not data:
            abort(400, "Not a JSON")
    except BadRequest:
        abort(400, "Not a JSON")
    if "email" not in data:
        abort(400, "Missing email")
    if "password" not in data:
        abort(400, "Missing password")
    new_user = User(**data)
    new_user.save()
    res = jsonify(new_user.to_dict())
    return make_response(res, 201)


@app_views.route("/users/<user_id>", methods=["PUT"], strict_slashes=False)
def update_user(user_id):
    """
    Update a specific User object in the database by its unique ID.

    This function locates a User object using the provided ID and updates
    its information with the data received from the request.
    If the update is successful, the function returns the updated User
    object along with a 200 HTTP status code.
    If the update fails due to invalid data,
    a 400 HTTP status code is returned.
    If the User object with the specified ID does not exist,
    a 404 HTTP status code is returned.

    Parameters:
    - user_id (int or str): The unique identifier
    of the User object to be updated.

    Returns:
    - user: The updated User object if the update is successful.
    - int: An HTTP status code of 200 for a successful update,
    400 for invalid data, or 404 if the User object is not found.
    """
    user = storage.get(User, str(user_id))
    if not user:
        abort(404)
    try:
        data = request.get_json(silent=True)
        if not data:
            abort(400, "Not a JSON")
    except BadRequest:
        abort(400, "Not a JSON")

    ignore_keys = ["id", "created_at", "updated_at", "email"]
    for key, val in data.items():
        if key not in ignore_keys:
            setattr(user, key, val)
    user.save()
    res = jsonify(user.to_dict())
    return make_response(res, 200)
