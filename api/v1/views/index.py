#!/usr/bin/python3

"""Index views for our app, containing Status"""

from flask import Flask as F, jsonify
from api.v1.views import app_views as AV


index = F(__name__)


@AV.route('/status', strict_slashes=False)
def get_status():
    """ Get Status and if 200, display 200, OK as json response """
    return jsonify({"status": "OK"})

if __name__ == '__main__':
        pass