#!/usr/bin/python3
"""
Route for handling User objects and operations
"""
from flask import jsonify, abort, request
from api.v1.views import app_views, storage
from models.user import User


@app_views.route("/users", methods=["GET"], strict_slashes=False)
def user_get_all():
    """
    Retrieves all User objects

    :return: JSON of all users
    """
    # Create a list to store user objects
    user_list = []
    # Get all user objects from the storage
    user_obj = storage.all("User")
    # Iterate over the user objects and append their JSON representation to the list
    for obj in user_obj.values():
        user_list.append(obj.to_json())

    # Return the list of user objects as JSON
    return jsonify(user_list)


@app_views.route("/users", methods=["POST"], strict_slashes=False)
def user_create():
    """
    Create user route

    :return: newly created user object
    """
    # Get the JSON data from the request
    user_json = request.get_json(silent=True)
    # Check if the request is a valid JSON
    if user_json is None:
        abort(400, 'Not a JSON')
    # Check if the email and password fields are present in the JSON data
    if "email" not in user_json:
        abort(400, 'Missing email')
    if "password" not in user_json:
        abort(400, 'Missing password')

    # Create a new User object using the JSON data
    new_user = User(**user_json)
    # Save the new user object to the storage
    new_user.save()
    # Create a response with the JSON representation of the new user object and a status code of 201 (Created)
    resp = jsonify(new_user.to_json())
    resp.status_code = 201

    return resp


@app_views.route("/users/<user_id>", methods=["GET"], strict_slashes=False)
def user_by_id(user_id):
    """
    Gets a specific User object by ID

    :param user_id: user object ID
    :return: user object with the specified ID or error
    """
    # Get the user object with the specified ID from the storage
    fetched_obj = storage.get("User", str(user_id))

    # If the user object is not found, return a 404 error
    if fetched_obj is None:
        abort(404)

    # Return the JSON representation of the user object
    return jsonify(fetched_obj.to_json())


@app_views.route("/users/<user_id>", methods=["PUT"], strict_slashes=False)
def user_put(user_id):
    """
    Updates a specific User object by ID

    :param user_id: user object ID
    :return: user object and 200 on success, or 400 or 404 on failure
    """
    # Get the JSON data from the request
    user_json = request.get_json(silent=True)

    # Check if the request is a valid JSON
    if user_json is None:
        abort(400, 'Not a JSON')

    # Get the user object with the specified ID from the storage
    fetched_obj = storage.get("User", str(user_id))

    # If the user object is not found, return a 404 error
    if fetched_obj is None:
        abort(404)

    # Update the attributes of the user object with the values from the JSON data
    for key, val in user_json.items():
        if key not in ["id", "created_at", "updated_at", "email"]:
            setattr(fetched_obj, key, val)

    # Save the updated user object to the storage
    fetched_obj.save()

    # Return the JSON representation of the updated user object
    return jsonify(fetched_obj.to_json())


@app_views.route("/users/<user_id>", methods=["DELETE"], strict_slashes=False)
def user_delete_by_id(user_id):
    """
    Deletes a User object by ID

    :param user_id: user object ID
    :return: empty dict with 200 or 404 if not found
    """
    # Get the user object with the specified ID from the storage
    fetched_obj = storage.get("User", str(user_id))

    # If the user object is not found, return a 404 error
    if fetched_obj is None:
        abort(404)

    # Delete the user object from the storage
    storage.delete(fetched_obj)
    # Save the changes to the storage
    storage.save()

    # Return an empty JSON response
    return jsonify({})
