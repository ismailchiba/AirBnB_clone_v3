from api.v1.views import app_views
from flask import jsonify

@app_views.get('/status')
def get_status():
    """gets status in json format"""
    return jsonify({"status": "OK"})
