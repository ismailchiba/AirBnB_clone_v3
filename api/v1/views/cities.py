#!usr/bin/python3
"""
Creates new view for City obj that handles all the restful API
"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.city import City

@app_views.route('/cities', methods=['GET'], strict_slashes=False)
def get_all_cities():
    cities = storage.all(City).values()
    city_json = [city.to_dict() for city in cities]
    return jsonify(city_json)