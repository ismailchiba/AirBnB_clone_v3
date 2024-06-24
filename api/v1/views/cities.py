#!/usr/bin/python3
"""
route for handling Cities objects and operations
"""
from flask import jsonify, abort, request
from api.v1.views import app_views, storage
from models.state import City


@app_viewa.route("/states/<state_id>/cities", methods=["GET"], strict_slashes=False)
def get_cities(state_id):
    """
    Retrieves all city objects from the state and returns
    information in json.
    """


