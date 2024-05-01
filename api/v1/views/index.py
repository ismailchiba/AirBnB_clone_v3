#!/usr/bin/python3
"""
    This is the index page handler for Flask.
"""
from flask import Flask, make_response, jsonify
from models import storage
from api.v1.views import app_views
from os import getenv
from flask_cors import CORS

classes = {"amenities": "Amenity",
           "cities": "City",
           "places": "Place",
           "reviews": "Review",
           "states": "State",
           "users": "User"}


@app_views.route('/status')
def status():
    """
        Flask route at /status.
        Displays the status of the API.
    """
    return {"status": "OK"}


@app_views.route('/stats')
def stats():
    """
        Flask route at /stats.
        Displays the number of each objects by type.
    """
    return {k: storage.count(v) for k, v in classes.items()}
