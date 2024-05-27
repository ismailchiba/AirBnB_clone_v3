#!/usr/bin/python3
"""Routing of the index file"""


from api.v1.views import app_views
from flask import jsonify


@app_views.route('/status', methods=['GET'])
def status():
    """Variable app_views which is an
    instance of Blueprint url prefix
    """
    return jsonify({"status": "OK"})
