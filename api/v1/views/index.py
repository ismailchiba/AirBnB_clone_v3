#!/usr/bin/python3
"""
@author: Edogun Peter Putech
"""
from api.v1.views import app_views
from flask import jsonify, Blueprint
from models import storage


@app_views.route('/status', methods=['GET'], strict_slashes=False)
def get_status():
    """ get status of the route """
    return jsonify({"status": "OK"})
