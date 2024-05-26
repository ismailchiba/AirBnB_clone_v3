#!/usr/bin/python3
""" endpoint (route) will be to return the status of your API
"""

from flask import Flask
from models import storage
from api.v1.views import app_views

app = Flask(__name__)


@app.teardown_appcontext
def teardown_appcontext(exception):
    """Close the storage engine"""
    storage.close()

app.register_blueprint(app_views)


if __name__ == "__main__":
    host = os.getenv('HBNB_API_HOST', '0.0.0.0')
    port = int(os.getenv('HBNB_API_PORT', 5000))
    app.run(host=host, port=port, threaded=True)
