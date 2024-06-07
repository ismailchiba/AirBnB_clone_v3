#!/usr/bin/python3
"""
module index
- app_views router
"""
from models import storage
from api.v1.views import app_views
from flask import jsonify


@app_views.route('/status')
def status():
    """ Status of API """
    return jsonify({"status": "OK"})
