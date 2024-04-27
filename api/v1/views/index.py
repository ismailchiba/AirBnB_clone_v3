#!/usr/bin/python3
""" index file for the project """


from . import app_views
from flask import jsonify


@app_views.route('/api/v1/status', methods=['GET'], strict_slashes=False)
def status():
    """ the ok status """
    return jsonify({'status': "OK"})
