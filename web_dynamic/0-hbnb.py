#!/usr/bin/python3
"""
Flask app to generate complete html page containing location/amenity
"""

from flask import Flask, render_template
from models import storage
import uuid
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.state import State


app = Flask(__name__)
app.url_map.strict_slashes = False


@app.teardown_appcontext
def close_db(error):
    """
    Remove the current SQLAlchemy Session
    """
    storage.close()


@app.route('/1-hbnb/')
def hbnb():
    """
    HBNB
    """
    states = storage.all(State).values()
    states = sorted(states, key=lambda k: k.name)

    st_ct = []
    for state in states:
        st_ct.append([state, sorted(state.cities, key=lambda k: k.name)])

    amenities = storage.all(Amenity).values()
    amenities = sorted(amenities, key=lambda k: k.name)
    cache_id = str(uuid.uuid4())

    return render_template('0-hbnb.html',
                           states=states,
                           amenities=amenities,
                           places=places,
                           cache_id=cache_id)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
