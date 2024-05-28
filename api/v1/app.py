#!/usr/bin/python3

""" Create a flask app and register the blueprint app_views """
from flask import Flask
from flask_cors import CORS
from api.v1.views import app_views
from models import storage

app = Flask(__name__)

CORS(app, resources={r"/*": {"origins": "0.0.0.0"}})

app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown(exception):
"""teardown function"""
    storage.close()

if __name__ == "__main__":
    app.run(getenv("HBNB_API_HOST"), getenv("HBNB_API_PORT"))
