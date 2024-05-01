from api.v1.views import app_views
from models import storage
from flask import abort, jsonify, request

from models.state import State


@app_views.route('/states', methods=['GET', 'POST'])
def states():
    if request.method == 'POST':
        kwargs = request.get_json()
        if kwargs is None:
            return {"error": "Not a JSON"}, 400
        if "name" not in kwargs:
            return {"error": "Missing name"}, 400
        new_state = State(**kwargs)
        new_state.save()
        return jsonify(new_state.to_dict()), 201

    elif request.method == 'GET':
        states = [state.to_dict() for state in storage.all("State").values()]
        return jsonify(states)


@app_views.route('/states/<int:id>', methods=['GET', 'DELETE', 'PUT'])
def states_id(id):
    state = storage.get(State, id)
    if state:
        if request.method == 'DELETE':
            state.delete()
            storage.save()
            return jsonify({}), 200

        elif request.method == 'PUT':
            kwargs = request.get_json()
            if kwargs is None:
                return {"error": "Not a JSON"}, 400
            for k, v in kwargs.items():
                if k not in ["id", "created_at", "updated_at"]:
                    setattr(state, k, v)
            state.save()
            return jsonify(state.to_dict()), 200

        return jsonify(state.to_dict()), 200

    return jsonify({"error": "State not found"}), 404
