#!/usr/bin/python3
'''Handles City objects for RESTful API actions'''

from models import storage
from models.city import City
from models.state import State
from api.v1.views import app_views
from flask import request, abort, jsonify


@app_views.route('/states/<state_id>/cities', methods=['GET'],
                 strict_slashes=False)
def all_cities(state_id):
    '''gets and creates objects of City object'''
    if request.method == 'GET':
        state = storage.get(State, state_id)
        if not state:
            abort(404)
        cities = [city.to_dict() for city in state.cities]
        return jsonify(cities)
