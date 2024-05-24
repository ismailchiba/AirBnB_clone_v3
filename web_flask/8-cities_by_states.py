#!/usr/bin/python3
"""TASK 9 Simble flask app"""
from flask import Flask, render_template
from models import storage

# Create a new Flask web application
app = Flask(__name__)


@app.teardown_appcontext
def shutdown_session(exception=None):
    """reload storage after each request"""
    storage.close()


@app.route("/cities_by_states", strict_slashes=False)
def cities_list():
    """list cities of each state sorted by name"""
    states = storage.all("State").values()
    return render_template('8-cities_by_states.html', states=states)


if __name__ == "__main__":
    # Run the Flask application
    app.run(host="0.0.0.0", port=5000)
