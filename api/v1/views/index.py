#!/usr/bin/python3
from api.v1.views import app_views
from flask import jsonify
from models import storage


@app_views.route(/status)
def status():
    return jsonify({"status": "OK"})


@app_views.route('/stats')
def get_stats():
    """ Retrieve the number of objects by type """
    stats = {}
    for obj_type in storage.all().keys():
        count = storage.count(obj_type)
        stats[obj_type] = count
    return jsonify(stats)
