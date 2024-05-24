#!/usr/bin/python3
"""TASK 10 Simble flask app"""
from flask import Flask, render_template
from models import storage

# Create a new Flask web application
app = Flask(__name__)


@app.teardown_appcontext
def shutdown_session(exception=None):
    """reload storage after each request"""
    storage.close()


@app.route('/hbnb_filters', strict_slashes=False)
def hbnb_filters():
    """list states of each state sorted by name"""
    states = storage.all("State")
    amenities = storage.all("Amenity")
    return render_template('10-hbnb_filters.html', states=states, amenities=amenities)


if __name__ == "__main__":
    # Run the Flask application
    app.run(host="0.0.0.0", port=5000)
