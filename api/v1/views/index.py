#!/usr/bin/python3
"""create Flask app; index file"""
from flask import Flask, jsonify
from api.v1.views import app_views
from models import storage

@app_views.route('/status', methods=['GET'], strict_slashes=False)
def api_status():
    """Restful API status"""
    response = ({"status":  "OK"})
    return jsonify(response)

@app_views.route('/stats')
def get_stats():
    '''
    
    '''
    stats={
        'amenties': storage.count('Amenity'),
        'cities': storage.count('City'),
        'places': storage.count('Place'),
        'reviews': storage.count('Review'),
        'states': storage.count('State'),
        'users': storage.count('User'),
    }
    return jsonify(stats)

