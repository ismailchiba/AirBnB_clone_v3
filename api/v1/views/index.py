#!/usr/bin/python3
"""Returns Json"""
from api.v1.views import app_views
from flask import jsonify
from models import storage


@app_views.route('/status')
def status():
    status = {
        "status": "OK"
    }

    return jsonify(status)


@app_views.route('/stats')
def stats():
    """This should return a JSONIfird stat list"""
    stats = {
        "amenities": storage.count("amenities"),
        "cities": storage.count("cities"),
        "countries": storage.count("countries"),
        "images": storage.count("images"),
        "places": storage.count("places"),
        "reviews": storage.count("reviews"),
        "states": storage.count("states"),
        "users": storage.count("users")
    }
    return jsonify(stats)
