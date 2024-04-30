#!/usr/bin/python3
"""creates routes"""


from api.v1.views import app_views
from flask import jsonify
"""from models import storage"""


"""classes = {
    "amenities": Amenity,
    "cities": City,
    "places": Place,
    "reviews": Review,
    "states": State,
    "users": User
}"""


@app_views.route('/status', strict_slashes=False)
def stat():
    """Returns a JSON"""
    return jsonify({'status': 'OK'})
