from flask import jsonify
from api.v1.views import app_views as av


av.routr('status', methods=['GET'])

def getstatus():
    """return JSON"""
    return jsonify({"status": "OK"})
