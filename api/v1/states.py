#!/usr/bin/python3
'''
Createw Flask app;and register the blueprint app_views to Flask instance app.
'''
from flask import jsonify, request
from api.v1.views import app_views
from models import storage
from models.state import State


# Route to list all states
@app_views.route('/states', methods=['GET'], strict_slashes=False)  # Corrected route
def list_states():
    """Retrieve the list of all State objects"""
    states = [state.to_dict() for state in storage.all(State).values()]
    return jsonify(states), 200


# Route to retrieve a specific state by ID
@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def get_state(state_id):
    """Retrieve a State object by its ID"""
    state = storage.get(State, state_id)
    if not state:
        return jsonify({"error": "Not found"}), 404
    return jsonify(state.to_dict()), 200  # Corrected 'to_dict()'


# Route to create a new state
@app_views.route('/states', methods=['POST'], strict_slashes=False)
def create_state():
    """Create a new State object"""
    if not request.is_json:
        return jsonify({"error": "Not a JSON"}), 400

    data = request.get_json()
    if "name" not in data:
        return jsonify({"error": "Missing name"}), 400

    new_state = State(name=data["name"])
    storage.new(new_state)
    storage.save()

    return jsonify(new_state.to_dict()), 201


# Route to update a state by ID
@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def update_state(state_id):
    """Update a State object"""
    state = storage.get(State, state_id)
    if not state:
        return jsonify({"error": "Not found"}), 404

    if not request.is_json:
        return jsonify({"error": "Not a JSON"}), 400

    data = request.get_json()
    for key, value in data.items():
        if key not in ["id", "created_at", "updated_at"]:
            setattr(state, key, value)

    storage.save()
    return jsonify(state.to_dict()), 200


# Route to delete a state by ID
@app_views.route('/states/<state_id>', methods=['DELETE'], strict_slashes=False)
def delete_state(state_id):
    """Delete a State object"""
    state = storage.get(State, state_id)
    if not state:
        return jsonify({"error": "Not found"}), 404

    storage.delete(state)
    storage.save()

    return jsonify({}), 200
