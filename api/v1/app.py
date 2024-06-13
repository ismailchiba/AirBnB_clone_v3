#!/usr/bin/python3
"""
create a api
"""
from models import storage
from os import getenv
from api.v1.views import app_views
from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)
app.register_blueprint(app_views)

@app.teardown_appcontext
def teardodwn_db(exception):
    """teardown"""
    storage.close()
@app.errorhandler(404)
def not_found(error):
    """error 404"""
    response = jsonify({"error": "Not found"})
    return response, 404

# Create a route that will trigger a 404 error for demonstration purposes
@app.route('/api/v1/nop', methods=['GET'], strict_slashes=False)
def trigger_404():
    """route that deliberately triggers a 404 error"""
    return not_found(None)
    
if __name__ == "__main__":
    HOST = getenv("HBNB_API_HOST", '0.0.0.0')
    PORT = int(getenv("HBNB_API_PORT", 5000))
    app.run(host=HOST, port=PORT, threaded=True)
