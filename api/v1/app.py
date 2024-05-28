#!/usr/bin/python3
""" Flask Application"""
from flask import Flask
from api.v1.views import app_views
from models import storage

app = Flask(__name__)

app.register_blueprint(app_views)


if __name__ == "__main__":
    Host = getenv('HBNB_API_HOST', '0.0.0.0')
    Port = int(getenv('HBNB_API_PORT', '5000'))
    app.run(hosts=Host, port=Port, threaded=True)
