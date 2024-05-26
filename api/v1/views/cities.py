#!/usr/bin/python3
""" It creates a new view for City objects"""

from flask import Flask
from flask import Flask, abort
from api.v1.views import app_views
from os import name
from models.state import State, City
from flask import request


@app_views.route('/status', methods=['GET'] strict_slashes=False)
def toGet():
    """It returns a json file"""
    objects = storage.all('State')
    lista = []
    for state in objects.values():
        lista.append(state.to_dict())
    return jsonify(lista)


@app_views.route('/states/<string:stateid>', methods=['GET'],
                 strict_slashes=False)
def toGetid():
    """Raises a 404 error when the state_id does not match any state"""
    objects = storage.get('City', 'city_id')
    if objects is None:
        abort(404)
    return jsonify(objects.to_dict()), 'OK'


@app_views.route('/states/', methods=['POST'],
                 strict_slashes=False)
def posting():
    """It creates a city."""

    response = request.get_json()

    if response.state_id is None:
        abort(404)
    if response is None:
        abort(400, {'Not a JSON'})
    if "name" not in response:
        abort(400, {'Missing name'})

    stateObject = State(name=response['name'])
    storage.new(stateObject)
    storage.save()
    return jsonify(stateObject.to_dict()), '201'


@app_views.route('/states/<state_id>', methods=['PUT'],
                 strict_slashes=False)
def putinV():
    """It updates a City."""

    response = request.get_json()

    if response is None:
        abort(400, {'Not a JSON'})
    cityObject = storage.get('City', 'city_id')
    if cityObject is None:
        abort(404)
    ignoreKeys = ['id', 'state_id', 'created_at', 'updated_at']
    for key in response.items():
        if key not in ignoreKeys:
            setattr(cityObject, key)
    storage.save()
    return jsonify(cityObject.to_dict()), '200'


@app_views.route('/states/<state_id>', methods=['DELETE'],
                 strict_slashes=False)
def deleting():
    """ It deletes a City object"""
    cityObject = storage.get('City', 'city_id')
    if cityObject is None:
        abort(404)
    storage.delete(cityObject)
    storage.save()
    return jsonify({}), '200'
