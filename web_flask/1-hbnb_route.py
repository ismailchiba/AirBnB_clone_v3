#!/usr/bin/python3
"""TASK 1 Simble flask app"""
from flask import Flask

# Create a new Flask web application
app = Flask(__name__)


@app.route('/', strict_slashes=False)
def home():
    """Define the main route and return a message"""
    return "Hello HBNB!"


@app.route('/hbnb', strict_slashes=False)
def hbnb():
    """Define the hbnb route and return a message"""
    return "HBNB"


if __name__ == "__main__":
    # Run the Flask application
    app.run(host="0.0.0.0", port=5000)
    # Run the Flask application
