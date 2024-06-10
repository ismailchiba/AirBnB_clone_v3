from api.v1.views app_views
from flask import jsonify
@app_views.route('/status', methods=['GET'])
def status():
    """returns a JSON: "status": "OK"."""
    return jsonify({"status": "OK"})
