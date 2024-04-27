#!/usr/bin/python3
""" index file for the project """


from . import app_views
from flask import jsonify


@app_views.route('/status', methods=['GET'], strict_slashes=False)
def status():
    """ the ok status """
    return jsonify({'status': "OK"})


@app_views.route('/api/v1/stats', methods=['GET'], strict_slashes=False)
def stats():
    """ the stats count """
    return jsonify(storage.count())
