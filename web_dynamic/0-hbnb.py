#!/usr/bin/python3
""" Starts Flash Web Application """
from flask import Flask, render_template
from models import Storage
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from os import environ
import uuid

app = Flask(__name__)


@app.teardown_appcontext
def close_db(error):
    """ close current SQLAlchemy Session """
    storage.close()


@app.route('/0-hbnb/', strict_slashes=False)
def hbnb():
    """ Web display HBNB """
    states = storage.all(State).values()
    states = sorted(states, key=lambda k: k.name)
    state_city = []
    
    for state in states:
        state_city.append([state, sorted(state.cities, key=lambda k: k.name)])

    amenities = storage.all(Amenity).values()
    amenities = sorted(amenities, key=lambda k: k.name)

    places = storage.all(Place).values()
    places = sorted(places, key=lambda k: k.name)

    return render_template('0-hbnb.html',
                            states=state_city,
                            amenities=amenities,
                            places=places,
                            cache_id = str(uuid.uuid4()))


    if __name__ == "__main__":
    """ Scripting on port 5000 """
    app.run(host='0.0.0.0', port=5000)
