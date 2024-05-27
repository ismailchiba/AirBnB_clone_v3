#!/usr/bin/python3
""" The Index. """


from api.v1.views import app_views
from flask import jsonify
from models import storage


@app_views.route('/status')
def api_status():
    """ Status of API  return: response with json."""
    responce = {'status': "OK"}
    return jsonify(responce)


@app_views.route('/stats')
def get_status():
    """Retrieves the number of each objects by type."""
    stats = {
        'amenities': storage.count('Amenity'),
        'cities': storage.count('City'),
        'places': storage.count('Place'),
        'reviews': storage.count('Review'),
        'states': storage.count('State'),
        'users': storage.count('User'),
    }

    return jsonify(stats)
