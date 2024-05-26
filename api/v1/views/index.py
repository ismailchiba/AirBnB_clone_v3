from flask import jsonify
from api.v1.views import app_views


# define the rute /status on the app_views Blueprint
@app_views.route('/status', methods=['GET'])
def get_status():
    # Return a JSON response with
    return jsonify({'status': 'OK'})
