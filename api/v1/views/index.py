from flask import jsonify
from api.v1.views import app_views

"""Create an instance of Blueprint with the URL prefix /api/v1"""

@app_views.route('/status')
def status():
    """
    Returns a JSON response with the status "OK".

    Returns:
        Response: A JSON response with the status "OK".
    """
    response = {"status": "OK"}
    return jsonify(response)
