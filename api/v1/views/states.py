from flask import jsonify, abort, make_response
from api.v1.views import app_views
from models import storage
from models.state import State

@app_views.route('/states', methods=['GET'], strict_slashes=False)
def get_states():
    """Retrieves the list of all State objects"""
    return jsonify(
        [
            states.to_dict()
            for states in storage.all(State).values()
        ]
    )

@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def get_state(state_id):
   """Retrieves a State object"""
    try:
        return jsonify(storage.get('State', state_id).to_dict())
    except Exception:
        abort(404)

@app_views.route('/states/<state_id>', methods=['DELETE'], strict_slashes=False)
def delete_state(state_id):
   """Deletes a State object"""
    try:
        storage.delete(storage.get('State', state_id))
        return make_response(jsonify({}), 200)
    except Exception:
        abort(404)

@app_views.route('/states', methods=['POST'], strict_slashes=False)
def create_state():
    """Creates a State"""
    if not request.json:
        abort(400)
        return jsonify({"error": "Not a JSON"})
    if 'name' not in request.json:
        abort(400)
        return jsonify({"error": "Missing name"})
    new_s = State(**request.get_json())
    new_s.save()
    return jsonify(new_s.to_dict()), 201

@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def update_state(state_id):
   """Updates a State object"""
    state = storage.get('State', state_id)
    if state is None:
        abort(404)
    if not request.json:
        return jsonify({"error": "Not a JSON"}), 400
    for key, value in request.get_json().items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(state, key, value)
    state.save()
    return jsonify(state.to_dict())
