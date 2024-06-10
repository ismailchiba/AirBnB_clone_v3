#!/usr/bin/python3
"""
    Handles all default RESTFul API actions for State objects
"""
from api.v1.views import app_views
from flask import abort, request, Response
import json
from models import storage
from models.state import State


@app_views.route("/states", strict_slashes=False)
def all_states():
    """
        Returns all states
    """
    all_states = storage.all(State)
    state_list = list()
    for each_state_key in all_states.keys():
        state_dict = all_states[each_state_key].to_dict()
        state_list.append(state_dict)
    json_format = json.dumps(state_list, indent=2)
    return Response(json_format, mimetype="application/json")


@app_views.route("/states/<state_id>", strict_slashes=False)
def match_id_state(state_id):
    """
        Shows a state object
    """
    all_states = storage.all(State)
    for each_state_key in all_states.keys():
        state_dict = all_states[each_state_key].to_dict()
        if state_id == state_dict["id"]:
            json_format = json.dumps(state_dict, indent=2)
            return Response(json_format, mimetype="application/json")
    abort(404)


@app_views.route("/states/<state_id>", methods=["DELETE"])
def delete_state(state_id):
    """
        Deletes a state object
    """
    keep_key = None
    all_states = storage.all(State)
    for each_state_key in all_states.keys():
        state_dict = all_states[each_state_key].to_dict()
        if state_id == state_dict["id"]:
            keep_key = each_state_key
            break
    if keep_key:
        storage.delete(all_states[each_state_key])
        storage.save()
        json_format = json.dumps({})
        return Response(json_format, mimetype="application/json", status=200)
    abort(404)


@app_views.route("/states", strict_slashes=False, methods=["POST"])
def post_state():
    """
        Creates and post new state
    """
    try:
        data = request.get_json()  # if fails, data is None
    except Exception:
        return "Not a JSON", 400
    name = data.get("name")
    if not name:
        return "Missing name", 400
    new_instance = State(name=name)
    new_instance.save()
    new_instance_json = json.dumps(new_instance.to_dict(), indent=2)
    return Response(new_instance_json, mimetype="application/json", status=201)


@app_views.route("/states/<state_id>", strict_slashes=False, methods=["PUT"])
def update_state(state_id):
    """
        Updates a state object
    """
    try:
        data = request.get_json()
    except Exception:
        return "Not a JSON", 400
    all_states = storage.all(State)
    for each_state_key in all_states.keys():
        state_dict = all_states[each_state_key].to_dict()
        if state_id == state_dict["id"]:
            instance = all_states[each_state_key]
            for key, value in data.items():
                if key == "id" or key == "created_at" or key == "updated_at":
                    continue
                setattr(instance, key, value)
            storage.save()
            instance_dict = instance.to_dict()
            instance_json = json.dumps(instance_dict, indent=2)
            return Response(instance_json, mimetype="application/json",
                            status=200)
    abort(404)
