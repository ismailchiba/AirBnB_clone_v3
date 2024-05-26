#!/usr/bin/python3

"""
An index module
"""

from api.v1.views import app_views
from flask import jsonify


@app_views.route("/status", strict_slashes=False)
def stat():
    '''
    returns the status of the page in json format
    '''
    return jsonify({"status": "OK"})
