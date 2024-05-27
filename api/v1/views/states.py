#!/usr/bin/python3
""" index routes """
from api.v1.views import app_views
from flask import jsonify, request, abort
from models import storage
from models.state import State


@app_views.route("/states")
def get_states():
    """get all states"""
    res = []
    for v in storage.all(State).values():
        res.append(v.to_dict())
    return jsonify(res)


@app_views.route("/stats")
def show_data():
    """count data"""
    total = {}
    for k, v in classes.items():
        total[k] = storage.count(v)
    return jsonify(total)


@app_views.route("/states/<state_id>")
def get_state(state_id: str):
    """get state"""
    res = storage.get(State, state_id)
    if res is None:
        abort(404)
    return jsonify(res.to_dict())


@app_views.route("/states/<state_id>", methods=["DELETE"])
def delete_state(state_id):
    """delete state"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    state.delete()
    storage.save()
    return jsonify({})


@app_views.route("/states", methods=["POST"])
def create_data():
    """add new state"""
    data = request.get_json()
    if not data:
        abort(400, "Not a JSON")
    if "name" not in data:
        abort(400, "Missing name")
    e = State(**data)
    e.save()
    return jsonify(e.to_dict()), 201


@app_views.route("/states/<state_id>", methods=["PUT"])
def update_state(state_id):
    """update state"""
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    data = request.get_json()
    if not data:
        abort(400, "Not a JSON")
    setattr(state, "name", request.get_json().get("name"))
    state.save()
    return jsonify(state.to_dict())
