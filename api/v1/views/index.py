#!/usr/bin/python3

"""Index views for our app, containing Status"""

from flask import Flask as F, jsonify, request as RQ
from api.v1.views import app_views as AV
from models import storage


index = F(__name__)


@AV.route('/status', methods=['GET'])
def get_status():
    """ Get Status and if 200, display 200, OK as json response """
    if RQ.method == 'GET':
        response = {"status": "OK"}
    return jsonify(response)


@AV.route('/stats', methods=['GET'])
def get_stats():
    stats = {}
    if RQ.method == 'GET':
        plurals ={
            'Amenity': 'amenities',
            'City': 'cities',
            'Place': 'places',
            'Review': 'reviews',
            'State': 'states',
            'User': 'users'
        }
        for key, value in plurals.items():
            stats[value] = storage.count(key)
            
    return jsonify(stats)
