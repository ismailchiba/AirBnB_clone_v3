#!/usr/bin/python3
""" this area is for description"""
from api.v1.views import app_views
from flask import make_response, jsonify


@app_views.route("/status", methods=['GET'])
def rt_ok():
    """ return api response status"""
    return jsonify({"status": "OK"})
