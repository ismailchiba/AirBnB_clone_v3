#!/usr/bin/python3
'''Manages state objects within the API.

   Handles retrieval, creation, deletion, and updates of state instances.
'''
from flask import jsonify, request
from werkzeug.exceptions import NotFound, MethodNotAllowed, BadRequest

from api.v1.views import app_views
from models import storage
from models.state import State


ALLOWED_METHODS = ['GET', 'DELETE', 'POST', 'PUT']
'''Methods allowed for the states endpoint.'''


@app_views.route('/states', methods=ALLOWED_METHODS)
@app_views.route('/states/<state_id>', methods=ALLOWED_METHODS)
def handle_states(state_id=None):
    '''Dispatches requests to appropriate state handler methods based on HTTP
        method and ID.

    Args:
        state_id (str, optional): ID of the state to get, delete, or update.
        Defaults to None.

    Returns:
        flask.json. jsonify: Response object with state data or error message.
    '''
    handlers = {
        'GET': get_states,
        'DELETE': remove_state,
        'POST': add_state,
        'PUT': update_state,
    }
    if request.method in handlers:
        return handlers[request.method](state_id)
    else:
        raise MethodNotAllowed(list(handlers.keys()))


def get_states(state_id=None):
    '''Retrieves state objects based on provided ID.

    If no ID is provided, returns a list of all state objects.
    If an ID is provided, returns the state object with that ID.

    Args:
        state_id (str, optional): ID of the state to retrieve. Defaults to None

    Returns:
        flask.json. jsonify: Response object with state data or error message.
    '''
    all_states = storage.all(State).values()
    if state_id:
        res = list(filter(lambda x: x.id == state_id, all_states))
        if res:
            return jsonify(res[0].to_dict())
        raise NotFound()
    all_states = list(map(lambda x: x.to_dict(), all_states))
    return jsonify(all_states)


def remove_state(state_id=None):
    '''Deletes a state object.

    Args:
        state_id (str, optional): ID of the state to delete. Defaults to None.

    Returns:
        flask.json. jsonify: Empty response object with status code 200.
    '''
    all_states = storage.all(State).values()
    res = list(filter(lambda x: x.id == state_id, all_states))
    if res:
        storage.delete(res[0])
        storage.save()
        return jsonify({}), 200
    raise NotFound()


def add_state(state_id=None):
    '''Creates a new state object.

    Args:
        state_id (str, optional): Ignored in this method. Defaults to None.

    Returns:
        flask.json. jsonify: Response object with data of the newly created
        state and status code 201.
    '''
    data = request.get_json()
    if type(data) is not dict:
        raise BadRequest(description='Not a JSON')
    if 'name' not in data:
        raise BadRequest(description='Missing name')
    new_state = State(**data)
    new_state.save()
    return jsonify(new_state.to_dict()), 201


def update_state(state_id=None):
    '''Updates an existing state object.

    Args:
        state_id (str, optional): ID of the state to update. Defaults to None.

    Returns:
        flask.json. jsonify: Response object with data of the updated state
        and status code 200.
    '''
    xkeys = ('id', 'created_at', 'updated_at')
    all_states = storage.all(State).values()
    res = list(filter(lambda x: x.id == state_id, all_states))
    if res:
        data = request.get_json()
        if type(data) is not dict:
            raise BadRequest(description='Not a JSON')
        old_state = res[0]
        for key, value in data.items():
            if key not in xkeys:
                setattr(old_state, key, value)
        old_state.save()
        return jsonify(old_state.to_dict()), 200
    raise NotFound()
