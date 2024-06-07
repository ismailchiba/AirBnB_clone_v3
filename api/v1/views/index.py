#!/usr/bin/python3
"""
module index
- app_views router
"""
from api.v1.views import app_views
from flask import jsonify
from models import storage

@app_views.route('/status')
def status():
    return jsonify({"status": "OK"})

@app_views.stat('/stats')
def stats():
    dic = {}
    obj = ["amenities", "cities", "places", "reviews", "states", "users"]
    for key in obj:
        dic[key] = storage.count(key)
    return dic
