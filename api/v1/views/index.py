#!/usr/bin/python3
""" A module containin routes in the index"""
from api.v1.views import app_views
from flask import jsonify


@app_views.route('/status', strict_slashes=False)
def check_status():
    """ Returns the status"""
    return jsonify({"status": "OK"})
