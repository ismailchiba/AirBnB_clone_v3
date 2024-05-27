#!/usr/bin/python3
""" Returns a JSON response """


from flask import jsonify
from api.v1.views import app_views


# define the rute /status on the app_views Blueprint
@app_views.route('/status')
def get_status():
    # Return a JSON response with
    """ Returns the no of each object by type """
    return jsonify({"status": "OK"})
