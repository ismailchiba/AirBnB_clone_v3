#!/usr/bin/python3
""" initiate the return of 'status: OK'"""

from api.v1.views import app_views
from flask import jsonify, Flask
from storage import count

@app_views.route('/status', methods=['GET'], strict_slashes=False)
def show():
    """ return "status": "OK" """
    return jsonify({"status": "OK"})

app = Flask(__name__)

@app.route('/api/v1/stats', methods=['GET'])
def retrieve():
    """retrieves the number of each objects by type"""
    counts = {
            "amenities": storage.count("amenities"),
            "cities": storage.count("cities"),
            "places": storage.count("places"),
            "reviews": storage.count("reviews"),
            "states": storage.count("states"),
            "users": storage.count("users")
            }
    return jsonify(counts)
