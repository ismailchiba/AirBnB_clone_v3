#!/usr/bin/python3
"""
Flask Application
Endpoint (route) will be to return the status of your API
"""


from flask import Flask
from models import storage
from api.v1.views import app_views
import os
from flask import jsonify


app = Flask(__name__)
app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown_db(exception):
    """Close the storage connection"""
    storage.close()


if __name__ == '__main__':
    """Run the Flask application"""
    host = os.getenv('HBNB_API_HOST', default='0.0.0.0')
    port = os.getenv('HBNB_API_PORT', default='5000')
    app.run(host=host, port=port, threaded=True)
