from flask import jsonify

from api.v1.views import app_views


@app_views.route('/status')
def status():
    """
    Route to return status OK in JSON format
    """
    return jsonify({"status": "OK"})
