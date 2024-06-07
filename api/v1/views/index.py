#!/usr/bin/python3
"""
Defines route for status used to check api availability
"""

from api.v1.views.__init__ import app_views
import json

#@app_views.route("/status", strict_slashes=False)
#def check_status():
@app_views.route("/status", methods=['GET'])
def status():
    """Returns status of api"""
    return jsonify({"status": "OK"})
