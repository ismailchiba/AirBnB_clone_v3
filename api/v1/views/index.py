#!/usr/bin/python3
""" The Index. """


from api.v1.views import app_views
from flask import jsonify


@app_views.route('/status')
def api_status():
    """ Status of API  return: response with json."""
    responce = {'status': "OK"}
    return jsonify(responce)
