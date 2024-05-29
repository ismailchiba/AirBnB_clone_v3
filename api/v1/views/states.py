from api.v1.views import app_views
from flask import jsonify, abort, request
from models.base_model import BaseModel
from models.state import State
from models import storage


@app_views.route("/states/")
@app_views.route("/states")
def get_states():
    """ return states """

    states_dict = []
    for value in storage.all(State).values():
        states_dict.append(value.to_dict())
    return jsonify(states_dict), 200


@app_views.route("/states/<state_id>")
@app_views.route("/states/<state_id>/")
def get_state(state_id):
    """ get state from provided ID"""

    states = storage.all(State).values()
    for state in states:
        if state.id == state_id:
            return jsonify(state.to_dict()), 200
    abort(404)


@app_views.route("/states/<state_id>", methods=['DELETE'])
@app_views.route("/states/<state_id>/", methods=['DELETE'])
def delete_state(state_id):
    """ delete state provided ID"""

    states = storage.all(State).values()
    for state in states:
        if state.id == state_id:
            storage.delete(state)
            storage.save()
            return jsonify({}), 200
    abort(404)


@app_views.route("/states/", methods=['POST'])
@app_views.route("/states", methods=['POST'])
def create_state():
    """ create state object"""

    obj_dict = request.get_json()
    if obj_dict is None:
        abort(400, "NOT a JSON")
    if "name" not in obj_dict.keys():
        abort(400, "Missing name")

    obj = State(**obj_dict)
    storage.new(obj)
    storage.save()
    x = obj.to_dict()
    return jsonify(x), 201


@app_views.route("/states/<state_id>", methods=["PUT"])
@app_views.route("/states/<state_id>/", methods=["PUT"])
def update_state(state_id):
    """ update state """

    skip_keys = ["id", "created_at", "updated_at"]
    for state in storage.all(State).values():
        if state.id == state_id:
            state_dict = state.to_dict()
            storage.delete(state)
            storage.save()
            update_info = request.get_json()
            if update_info is None:
                abort(400, "Not a JSON")
            for key, value in update_info.items():
                if key not in skip_keys:
                    state_dict[key] = value
            new_state = State(**state_dict)
            storage.new(new_state)
            storage.save()
            return jsonify(state_dict), 200
    abort(404)
