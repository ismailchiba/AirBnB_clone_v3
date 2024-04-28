#!/usr/bin/python3
'''let's configure flask status'''
from flask import jsonify
from api.v1.views import app_views
import models
from models.base_model import BaseModel


@app_views.route('/status', strict_slashes=False)
def status():
    ''' shows the status'''
    return jsonify(status='OK')

@app_views.route('/stats', strict_slashes=False)
def get_statistics():
    """
    Endpoint to retrieve statistics about different entities in storage.
    Returns a JSON response with counts for each entity.
    """
    entity_counts = {
        'states': storage.count(State),
        'users': storage.count(User),
        'amenities': storage.count(Amenity),
        'cities': storage.count(City),
        'places': storage.count(Place),
        'reviews': storage.count(Review)
    }
    return jsonify(entity_counts)

