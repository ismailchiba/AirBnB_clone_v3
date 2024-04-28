#!/usr/bin/python3

from flask import jsonify
from api.v1.views import app_views



# Route to return status "OK"
@app_views.route('/status', methods=['GET'])
def api_status():
        """
        """
        #response = {"status" :"OK"}
        #return jsonify(response)
        return jsonify({"status": "OK"})

