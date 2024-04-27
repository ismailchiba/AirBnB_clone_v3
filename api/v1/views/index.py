#!/usr/bin/python3
"""
let's get that status
"""
from models import storage
from api.v1.views import app_views
from flask import jsonify


@app_views.route('/status', methods=['GET'], strict_slashes=False)
def status():
    """ le's check the status """
    return jsonify({"status": "OK"})
