#!/usr/bin/python3
"""Import required module/lib"""
from flask import jsonify
from models import storage
from api.v1.views import app_views


@app_views.route('/states')
def get_states():
    """Retrieve all states"""
    states = storage.all("State")
    return jsonify([state.to_json() for state in states.values()])
