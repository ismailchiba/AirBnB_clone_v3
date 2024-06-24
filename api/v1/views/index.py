from flask import jsonify
from models import storage
from models import classes
from api.v1.views import app_views

@app_views.route("/status")
def status():
    """returns endpoint status"""
    return jsonify({ "status": "OK" })

@app_views.route("/stats")
def stats():
    """retrieves the number of each objects by type"""
    myobj = {}
    for k, v in classes.items():
        myobj[k.lower()] = storage.count(v)
    return jsonify(myobj)
