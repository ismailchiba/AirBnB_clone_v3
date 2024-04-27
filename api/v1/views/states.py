#!/usr/bin/python3
"""states module"""
from flask import jsonify, abort, request, make_response
from api.v1.views.index import app_views
from models import storage
from models.state import State


@app_views.route('/states', strict_slashes=False)
def a_sta():
	"""Return all states"""
	all_states = [x.to_dict() for x in storage.all("State").values()]
	if not all_states:
		return jsonify({})
	return jsonify(all_states)


@app_views.route('/states/<state_id>', strict_slashes=False, methods=['GET'])
def get_sta(state_id):
	"""Return a state"""
	s = storage.get(State, state_id)
	if s:
		return jsonify(s.to_dict())
	abort(404)


@app_views.route('/states/<state_id>', strict_slashes=False, methods=['DELETE'])
def delete_sta(state_id):
	if state_id:
		"""Delete a state"""
		s = storage.get(State, state_id)
		if s:
			s.delete()
			storage.save()
			return jsonify({})
	abort(404)


@app_views.route('/states/<state_id>', strict_slashes=False, methods=['PUT'])
def update_sta(state_id):
	"""Update a state"""
	if not state_id:
		abort(404)
	s = storage.get(State, state_id)
	if not s:
		abort(404)
	resp_body = request.get_json(silent=True)
	if not resp_body:
		return make_response(jsonify({"error": "Not a JSON"}), 400)
	for k, v in dict(resp_body).items():
		if k == "id" or k == "created_at" or k == "updated_at":
			continue
		setattr(s, k, v)
	storage.save()
	return jsonify(s.to_dict())


@app_views.route('/states', strict_slashes=False, methods=['POST'])
def create_sta():
	"""Create a state"""
	resp_body = request.get_json(silent=True)
	if not resp_body:
		return make_response(jsonify({"error": "Not a JSON"}), 400)
	if 'name' not in resp_body:
		return make_response(jsonify({"error": "Missing name"}), 400)
	obj = State(**resp_body)
	obj.save()
	return make_response(jsonify(obj.to_dict()), 201)


# #!/usr/bin/python3
# from flask import jsonify, request, abort, make_response
# from api.v1.views.index import app_views
# from models import storage
# from models.state import State


# @app_views.route('/states', strict_slashes=False)
# def retrieve_state():
#     """Retrieves the list of all State objects"""
#     all_states = [x.to_dict() for x in storage.all("State").values()]
#     if not all_states:
#         return jsonify({})
#     return jsonify(all_states)


# @app_views.route('/states/<state_id>', strict_slashes=False, methods=['GET'])
# def get_state(state_id):
#     """Retrieves a State object"""
#     state = storage.get(State, state_id)
#     if state:
#         return jsonify(state.to_dict())
#     abort(404)


# @app_views.route('/states/<state_id>',
#                  strict_slashes=False, methods=['DELETE'])
# def delete_state(state_id):
#     """Deletes a State object"""
#     state = storage.get(State, state_id)
#     if state:
#         state.delete()
#         storage.save()
#         return jsonify({})
#     abort(404)


# @app_views.route('/states', strict_slashes=False, methods=['POST'])
# def create_state():
#     """create new state"""
#     response = request.get_json(silent=True)
#     if not response:
#         return make_response(jsonify({"error": "Not a JSON"}), 400)
#     if 'name' not in response:
#         return make_response(jsonify({"error": "Missing name"}), 400)
#     new_state = State(**response)
#     new_state.save()
#     return make_response(jsonify(new_state.to_dict()), 201)


# @app_views.route('/states/<state_id>',
#                  strict_slashes=False, methods=['PUT'])
# def update_state(state_id):
#     """update states"""
#     if not state_id:
#         abort(404)
#     state = storage.get(State, state_id)
#     if not state:
#         abort(404)
#     response = request.get_json(silent=True)
#     if not response:
#         return make_response(jsonify({"error": "Not a JSON"}), 400)
#     for key, value in dict(response).items():
#         if key == "id" or key == "created_at" or key == "updated_at":
#             continue
#         setattr(state, key, value)
#     storage.save()
#     return jsonify(state.to_dict())
