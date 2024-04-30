#!/usr/bin/python3
""" A module containin routes in the index"""
from api.v1.views import app_views
from flask import jsonify
from models import storage

@app_views.route('/status', strict_slashes=False)
def check_status():
    """ Returns the status"""
    return jsonify({"status": "OK"})

@app_views.route('/stats', strict_slashes=False)
def get_stats():
    " Retrieves the number of each objects by type """
    all_cls = {}
    for classs in classes:
        value = storage.count(classs)
        all_cls[classs] = value
    return jsonify(all_cls)




