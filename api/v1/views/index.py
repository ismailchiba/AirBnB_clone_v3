#!/usr/bin/python3
"""
created Flask app: app_views
"""

from flask import jsonify
from api.v1.views import app_views

from models import storage


@app_views.route("/status", methods=['GET'])
def status():
    """
    status route
    :return: response with json
    """

    response = {'status':"OK"}
    return jsonify(response)
    # alternative
    # return jsonify({"status": "OK"})
    
