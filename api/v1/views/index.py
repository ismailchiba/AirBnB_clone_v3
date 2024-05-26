#!/usr/bin/python3xx
"""Script returns a JSON API status."""

import models
from models import storage
from models.base_model import BaseModel
from flask import jsonify
from api.v1.views import app_views


@app_views.route('/status', strict_slashes=False)
def returnstuff():
    """It returns a json api status."""
    return jsonify(status='OK')


@app_views.route('/stats', strict_slashes=False)
def stuff():
    """It returns a json object."""
    todos = {'states': State, 'users': User,
            'amenities': Amenity, 'cities': City,
            'places': Place, 'reviews': Review}
    for key in todos:
        todos[key] = storage.count(todos[key])
    return jsonify(todos)
