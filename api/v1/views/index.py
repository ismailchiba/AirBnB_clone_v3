#!/usr/bin/python3
"""This returns a Json response"""

from flask import jsonify
from api.v1.views import app_views
from models import storage


@app_views.route('/status')
def status_check():
    """This returns status code"""
    return jsonify({"status": "OK"})
