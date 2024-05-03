#!/usr/bin/python3
"""create flask app
"""
from flask import jsonify
from api.v1.views import app_views
from models import storage


@app_views.route('/status')
def api_status():
    """route thst returns a JSON status"""
    response = {'status': "OK"}
    return jsonify(response)


@app_views.route('/stats')
def get_stats():
    """ retrieves the number of each objects by type"""
    stats = {
            'amenities': storage.count('Amenities'),
            'cities': storage.count('Cities'),
            'places': storage.count('Place'),
            'reviews': storage.count('Review'),
            'states': storage.count('State'),
            'user': storage.count('User'),
    }

    return jsonify(stats)
