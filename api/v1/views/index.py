#!/usr/bin/python3
"""
index
"""

from api.v1.views import app_views
from flask import jsonify
from models import storage

#create a route /status on the object app_views that returns a JSON: "status": "OK"
@app_views.route('/status', methods=['GET'])
def status():
    answer = {"status": "OK"}
    return jsonify(answer)

#Create an endpoint that retrieves the number of each objects by type
@app_views.route('/stats', methods=['GET'])
def status():
    counts = {
            'amenities': storage.count('Amenity'),
            'cities': storage.count('City'),
            'places': storage.count('Place'),
            'reviews': storage.count('Review'),
            'states': storage.count('State'),
            'users': storage.count('User')
    }
    
    return jsonify(counts)



