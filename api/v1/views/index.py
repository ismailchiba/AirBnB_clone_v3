#!/usr/bin/python3

from flask import Flask, jsonify
from api.v1.views import app_views

@app_views.route('/status')
def app_return():
    """returns a JSON"""
    return (status='OK')

@app_views.route('/stats')
def status():
    """retrives the number of each objects by type"""
    storage = Storage()
    obj_counts = {}
    for obj_type in storage.types():
        obj_counts[obj_type] = storage.count(obj_type)
    return jsonify(obj_counts)
