#!/usr/bin/python3
"""The flask web application"""

from flask import jsonify
from flask import Flask
from models import storage
from app.v1.views import app_views

app = Flask(__name__)

app.register_blueprint(app_views)

@app.teardown_appcontext("/")
def teardown_flask():
    """closing the sqlalchemy session"""
    storage.close()


if __name__ == "__main__":
    app_host = ('HBNB_API_HOST', '0.0.0.0')
    app_port = ('HBNB_API_PORT', '5000')
    app.run(host = app_host,
            port = app_port,
            threaded=True
    )