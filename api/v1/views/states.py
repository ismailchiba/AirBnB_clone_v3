from api.v1.views import app_views
from flask import jsonify, abort, request
from models.base_model import BaseModel
from models.state import State
from models import storage
import json


@app_views.route("/states/")
def get_states():
    """ return states """

    states_dict = []
    for value in storage.all(State).values():
        states_dict.append(value.to_dict())
    return json.dumps(states_dict, indent=2) + '\n'


@app_views.route("/states/<state_id>")
def get_state(state_id):
    """ get state from provided ID"""

    states = storage.all(State).values()
    for state in states:
        if state.id == state_id:
            return json.dumps(state.to_dict(), indent=2) + '\n'
    abort(404)


@app_views.route("/states/<state_id>", methods=['DELETE'])
def delete_state(state_id):
    """ delete state provided ID"""

    states = storage.all(State).values()
    for state in states:
        if state.id == state_id:
            storage.delete(state)
            storage.save()
            return json.dumps({}, indent=2) + '\n'
    abort(404)

@app_views.route("/states/", methods=['POST'])
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
    return json.dumps(x, indent=2) + '\n', 201 


@app_views.route("/states/<state_id>", methods=["PUT"])
def put_update(state_id):
    """ update state """

    obj = storage.all(State)
    skip_keys = ["id", "created_at", "updated_at"]
    available = False
    for key in obj.keys():
        if key.split('.')[-1] == state_id:
            available = True
            state = obj[key]
            obj_dict = state.to_dict()
            break

    if available is False:
        abort(404)
    up_dict = request.get_json()
    if up_dict is None:
        abort(400, "Not a JSON")
    storage.delete(state)
    storage.save()
    for ky, value in up_dict.items():
        if ky not in skip_keys:
            obj_dict[ky] = value
    obj = State(**obj_dict)
    storage.new(obj)
    storage.save()
    return json.dumps(obj.to_dict(), indent=2) + '\n', 200
