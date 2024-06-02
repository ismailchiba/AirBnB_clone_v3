#!/usr/bin/python3
"""
Starts a Flask Web Application
"""
import uuid
from flask import Flask, render_template
from models import storage
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place

app = Flask(__name__)
app.url_map.strict_slashes = False

@app.teardown_appcontext
def close_db(error):
    """
    Remove the current SQLAlchemy Session
    """
    storage.close()

@app.route('/3-hbnb/')
def hbnb():
    """
    HBNB
    """
    # Fetch and sort states
    states = storage.all(State).values()
    states = sorted(states, key=lambda k: k.name)

    # Prepare states and cities data
    st_ct = []
    for state in states:
        st_ct.append([state, sorted(state.cities, key=lambda k: k.name)])

    # Fetch and sort amenities
    amenities = storage.all(Amenity).values()
    amenities = sorted(amenities, key=lambda k: k.name)

    # Fetch and sort places
    places = storage.all(Place).values()
    places = sorted(places, key=lambda k: k.name)

    # Generate a unique cache ID
    cache_id = str(uuid.uuid4())

    return render_template('3-hbnb.html',
                           states=st_ct,
                           amenities=amenities,
                           places=places,
                           cache_id=cache_id)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
