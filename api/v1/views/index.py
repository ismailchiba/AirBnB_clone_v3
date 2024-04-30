#!/usr/bin/python3

"""Index views for our app, containing Status"""

from flask import Flask as F, jsonify, request as RQ
from api.v1.views import app_views as AV


index = F(__name__)


@AV.route('/status', methods=['GET'])
def get_status():
    """ Get Status and if 200, display 200, OK as json response """
    if RQ.method == 'GET':
        response = {"status": "OK"}
    return jsonify(response)
