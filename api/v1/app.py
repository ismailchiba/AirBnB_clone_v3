#!/usr/bin/python3
# api/v1/app.py

from flask import Flask, jsonify
from models import storage
from api.v1.views import app_views

app = Flask(__name__)

# Register the blueprint to the Flask application
app.register_blueprint(app_views)

# Handle teardown for database connections
# 404 Error Handler
@app.errorhandler(404)
def not_found(error):
    """
    Returns a JSON response with a 404 status code.
    """
    return jsonify({"error": "Not found"}), 404

@app.teardown_appcontext
def close_storage(exc):
    """Close the storage on teardown."""
    storage.close()

# Run the Flask application with provided configurations
if __name__ == "__main__":
    import os
    
    host = os.getenv("HBNB_API_HOST", "0.0.0.0")
    port = int(os.getenv("HBNB_API_PORT", "5000"))
    
    app.run(host=host, port=port, threaded=True)
