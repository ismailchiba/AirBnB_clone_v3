#!/usr/bin/python3
"""The app module"""
from flask import Flask
from models import storage
from api.v1.views import app_views
from os import getenv
HOST = getenv("HBNB_API_HOST") or '0.0.0.0'
PORT = getenv("HBNB_API_PORT") or '5000'

app = Flask()
@app.register_blueprint(app_views)

@app.teardown_appcontext()
def teardown_appcontext(response_or_exc):
    """Close storage in when flask app finish its process"""    
    storage.close()

if __name__ == "__main__":
    app.run(host=HOST, port=PORT)
