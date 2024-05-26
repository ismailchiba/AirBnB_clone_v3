<<<<<<< HEAD
<<<<<<< HEAD
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
=======
=======
>>>>>>> dff4a60a4ac807bc9108c52bf6cb81f811eec8a5
#!/usr/bin/python3
"""
App views for AirBnB_clone_v3
"""

from flask import jsonify
from models import storage
from api.v1.views import app_views


@app_views.route('/status')
def status():
    """ returns status """
    status = {"status": "OK"}
    return jsonify(status)


@app_views.route('/stats')
def count():
    """ returns number of each objects by type """
    total = {}
    classes = {"Amenity": "amenities",
               "City": "cities",
               "Place": "places",
               "Review": "reviews",
               "State": "states",
               "User": "users"}
    for cls in classes:
        count = storage.count(cls)
        total[classes.get(cls)] = count
    return jsonify(total)
<<<<<<< HEAD
>>>>>>> dff4a60a4ac807bc9108c52bf6cb81f811eec8a5
=======
>>>>>>> dff4a60a4ac807bc9108c52bf6cb81f811eec8a5
