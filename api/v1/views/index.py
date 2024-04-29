#!/usr/bin/python3
<<<<<<< HEAD
"""
created Flask app: app_views
"""
=======
>>>>>>> storage_get_count

from flask import jsonify
from api.v1.views import app_views

<<<<<<< HEAD
from models import storage


@app_views.route("/status", methods=['GET'])
def status():
    """
    status route
    :return: response with json
    """
    #alternative
    response = {'status':"OK"}
    return jsonify(response)
    #return jsonify({"status": "OK"})
    
=======


# Route to return status "OK"
@app_views.route('/status', methods=['GET'])
def api_status():
        """
        """
        #response = {"status" :"OK"}
        #return jsonify(response)
        return jsonify({"status": "OK"})

>>>>>>> storage_get_count
