#!/usr/bin/python3
"""
    import app_views from api.v1.views
        create a route /status on the object app_views that returns a JSON: "status": "OK" (see example)
    """
from flask import jsonify
from app.v1.views import app_views
from models import storage

@app_views.route('/status', methods=['GET'])
def get_status():
    route_response = {"status": "OK"}
    return jsonify(route_response)


@app_views.route('/stats', methods=['GET'])
def get_stats():
    """_summary_

    Returns:
        _type_: _description_
    """
    route_response = {"amenities": storage.count("Amenity"),
                      "cities": storage.count("City"),
                      "places": storage.count("Place"),
                      "reviews": storage.count("Review"),
                      "states": storage.count("State"),
                      "users": storage.count("User")}
    return jsonify(route_response) 