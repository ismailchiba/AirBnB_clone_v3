#!/usr/bin/python3
""" This module returns status of API """
from api.v1.views import app_views


@app_views.route('/status', methods=['GET'], strict_slashes=False)
def status():
    """ Returns a JSON """
    return {"status": "OK"}


@app_views.route('/stats', methods=['GET'], strict_slashes=False)
def stats():
    """ Returns a JSON of the number of each object by type """
    from models import storage
    from models.state import State
    from models.city import City
    from models.amenity import Amenity
    from models.place import Place
    from models.review import Review
    from models.user import User

    classes = {"amenities": Amenity, "cities": City, "places": Place,
               "reviews": Review, "states": State, "users": User}
    return {key: storage.count(value) for key, value in classes.items()}
