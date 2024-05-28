#!/usr/bin/python3
"""Flask API to return route status of my api"""
from models import storage
from api.v1.views import app_views
from flask import Flask, render_template

app = Flask(__name__)

app.register_blueprint(app_views)

@app.teardown_appcontext
def teardown_appcontext(exception):
    """Teardown function"""
    storage.close()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
