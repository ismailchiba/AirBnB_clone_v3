#!/usr/bin/python3
"""create flask app"""
from flask import jsonify
from api.v1.views import app_views


@app_views.route('/status')
def api_status():
    """route thst returns a JSON status"""
    response = {'status': "OK"}
    return jsonify(response)
