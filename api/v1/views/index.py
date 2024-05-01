#!/usr/bin/python3
'''this is the index'''

from flask import jsonify
from api.v1.views import app_views

@app_views.route('/status')
def api_status():
    """
    this is the app status
    """

reponse = ('status': 'OK')
return jsonify(response)
