from flask import jsonify
from . import app_views

# Route to return status "OK"
@app_views.route('/status', methods=['GET'])
def get_status():
        return jsonify({"status": "OK"})

