#!/usr/bin/python3
from flask import request, abort, jsonify
from models import storage
from models.state import State
from api.v1.views import app_views


@app_views.route("/states", methods=["GET", "POST"])
def states():
    """Define /satets route with GET and POST methods

    POST - Create a new state
    GET - Get a list of all states
    """
    # GET
    if request.method == "GET":
        return jsonify([state.to_dict()
                        for state in storage.all("State").values()])
    # POST
    doc = request.get_json(silent=True)
    if doc is None:
        return "Not a JSON", 400
    if doc.get("name") is None:
        return "Missing name", 400
    state = State(**doc)
    state.save()
    return jsonify(state.to_dict()), 200


@app_views.route("/states/<state_id>", methods=["GET", "DELETE", "PUT"])
def state(state_id):
    """Define /state/<state_id> with GET, PUT and DELETE  methodes

    GET - get a state with the given id
    PUT - Update the state with the given id
    DELETE - Deletes the state with the givem id
    """
    state = storage.get('State', state_id)
    if state is None:
        abort(404)

    # GET
    if request.method == "GET":
        return jsonify(state.to_dict())

    # PUT
    elif request.method == "PUT":
        doc = request.get_json(silent=True)
        if doc is None:
            return "Not a JSON", 400

        for k, v in doc.items():
            if k not in ("id", "created_at", "updated_at"):
                setattr(state, k, v)
        state.save()
        return jsonify(state.to_dict())

    # DELETE
    state.delete()
    storage.save()
    return jsonify({})
