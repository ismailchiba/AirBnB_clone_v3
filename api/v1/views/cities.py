#!/usr/bin/python3
""" Cities view """

from api.v1.views import app_views
from flask import jsonify, abort
import models


@app_views.route('/states/<state_id>/cities',
                 methods=['GET'], strict_slashes=False)
def list_cities(state_id):
    """ return json of the cities of a given state """
    states = models.storage.all("State")
    key = f'State.{state_id}'
    state = states.get(key)
    if state is not None:
        cities = []
        for city in state.cities:
            cities.append(city.to_dict())
        return jsonify({"cities": cities})
    else:
        return abort(404)
