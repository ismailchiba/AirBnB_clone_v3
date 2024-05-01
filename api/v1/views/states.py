#!/usr/bin/python3
"""States view for the API."""
from flask import jsonify, abort, request, redirect, url_for, make_response
from models import storage
from models.state import State
from api.v1.views import app_views
from werkzeug.exceptions import BadRequest


@app_views.route("/states", methods=["GET"], strict_slashes=False)
@app_views.route("/states/<state_id>", methods=["GET"], strict_slashes=False)
def get_state(state_id=None):
    """Retrieves a State object.
    Retrieves the list of all State objects.
    """
    if state_id:
        state = storage.get(State, state_id)
        if state is None:
            abort(404)
        return jsonify(state.to_dict())
    else:
        all_states = storage.all(State).values()
        return jsonify([state.to_dict() for state in all_states])


@app_views.route(
    "/states/<state_id>", methods=["DELETE"], strict_slashes=False
)
def delete_state(state_id):
    """Deletes a State object."""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    storage.delete(state)
    storage.save()
    return jsonify({}), 200


@app_views.route("/states", methods=["POST"], strict_slashes=False)
def create_state():
    """Creates a State."""
    try:
        data = request.get_json()
        if "name" not in data or not data["name"].strip():
            abort(400, description="Missing name")
    except BadRequest:
        abort(400, description="Not a JSON")
    except Exception as e:
        abort(500)
    new_state = State(**data)
    storage.new(new_state)
    storage.save()
    response = jsonify(new_state.to_dict())
    response.status_code = 201
    response.headers["Location"] = url_for(
        "app_views.get_state", state_id=new_state.id, _external=True
    )
    return response



