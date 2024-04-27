#!/usr/bin/python3
"""creates routes"""


from api.v1.views import app_views
from flask import jsonify


@app_views.route('/status', methods=['GET'])
def stat():
    """Returns a JSON"""
    return jsonify({'status': 'OK'})
