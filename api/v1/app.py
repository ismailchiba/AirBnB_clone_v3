#!/usr/bin/python3
"""Creates web application"""

from flask import Flask
from models import storage
from api.v1.views import app_views
from os import getenv


host = getenv('HBNB_API_HOST', '0.0.0.0')
port = getenv('HBNB_API_PORT', 5000)

app = Flask(__name__)
app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown(exc):
    """Function closes the storage"""
    storage.close()


if __name__ == "__main__":
    app.run(debug=True, host=host, port=port, threaded=True)
