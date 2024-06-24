#!/usr/bin/python3
""" Starting flask application
Routes:

    /hbnb: display a HTML page like 8-index.html,
    done during the 0x01. AirBnB clone - Web static project
"""
from flask import Flask, render_template
from models import *
from models import storage

app = Flask(__name__)


@app.route('/hbnb', strict_slashes=False)
def hbnb_filters():
    """ Displays main HBnB html page """
    states = storage.all('State').values()
    amenities = storage.all('Amenity').values()
    places = storage.all('Place').values()
    return render_template('100-hbnb.html', states=states,
                           amenities=amenities, places=places)


@app.teardown_appcontext
def teardown(exception):
    """ Remove the current sqlalchemy session """
    storage.close()


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
