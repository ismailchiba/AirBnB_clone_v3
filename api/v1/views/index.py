#!/usr/bin/python3
'''
app views
'''

from flask import jsonify
from api.v1.views import app_views

@app_views.route('/status')
def api_status():
    """
    app def
    """
    response = {'status': : 'OK')
    return jsonify(response)
