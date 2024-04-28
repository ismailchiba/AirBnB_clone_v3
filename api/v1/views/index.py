from api.v1.views import app_views
from flask import jsonify


@app_views.route('/status', methods=['GET'])
def status():
    """status OK"""
    return jsonify({"status": "OK"})
