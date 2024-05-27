#!/usr/bin/python3
"""
To create all blueprints for our Flask web application
"""

from api.v1.views import app_views
import jsonify

@app_views.route('/status')
def status():
	" Returns the status of an application "
	return jsonify({"status": "OK"})
