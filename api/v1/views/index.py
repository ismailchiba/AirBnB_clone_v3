#!/usr/bin/python3
"""Status of my API"""
from api.v1.views import app_views
from flask import jsonify
from crypt import methods


@app_views.route('/status', strict_slashes=False)
def status():
    """ Shows http status """
    return jsonify({"status": "ok"})
