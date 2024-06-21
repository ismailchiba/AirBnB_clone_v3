#!/usr/bin/python3
"""API State view."""
from api.v1.views import app_views
from flask import abort, jsonify, request
from models import storage
from models.state import State


@app_views.route("/states", methods=["GET", "POST"])
def states():
    """Defines GET and POST methods for the states route."""

    if request.method == "GET":
        return jsonify([s.to_dict() for s in storage.all("State").values()])

    data = request.get_json(silent=True)
    if data is None:
        return "Not a JSON", 400
    if data.get("name") is None:
        return "Missing name", 400
    state = State(**data)
    state.save()
    return jsonify(state.to_dict()), 201


@app_views.route("/states/<state_id>", methods=["GET", "DELETE", "PUT"])
def state_id(state_id):
    """Defines GET, DELETE and PUT methodS"""
    state = storage.get("State", state_id)
    if state is None:
        abort(404)

    if request.method == "GET":
        return jsonify(state.to_dict())

    elif request.method == "DELETE":
        state.delete()
        storage.save()
        return jsonify({})

    data = request.get_json(silent=True)
    if data is None:
        return "Not a JSON", 400
    avoid = {"id", "created_at", "updated_at"}
    [setattr(state, k, v) for k, v in data.items() if k not in avoid]
    state.save()
    return jsonify(state.to_dict())
