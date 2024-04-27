#!/usr/bin/python3
""" A module that contains the flask app"""
from flask import Flask
from models import storage
from views import app_views


app = Flask(__name__)
app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown():
    """ closes the session """
    storage.close()


if __name__ == "__main__":
    app.run(debug=True, host=0.0.0.0, port=5000, threaded=True)
