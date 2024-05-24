#!/usr/bin/python3
"""TASK 5 Simble flask app"""
from flask import Flask, abort, render_template

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


@app.route('/c/<text>', strict_slashes=False)
def c_text(text):
    """Define the c route and return a message"""
    modified_text = text.replace('_', ' ')
    return f'C {modified_text}'


@app.route('/python', strict_slashes=False)
@app.route('/python/<text>', strict_slashes=False)
def python_text(text="is cool"):
    """Define the python route and return a message"""
    modified_text = text.replace('_', ' ')
    return f'Python {modified_text}'


@app.route('/number/<n>', strict_slashes=False)
def number(n):
    """Define the number route and return a message"""
    try:
        return f'{int(n)} is a number'
    except Exception:
        abort(404)


@app.route('/number_template/<n>', strict_slashes=False)
def number_template(n):
    """Define the number_template route and return a HTML page"""
    try:
        number = int(n)
        return render_template(f"5-number.html", number=number)
    except Exception:
        abort(404)


if __name__ == "__main__":
    # Run the Flask application
    app.run(host="0.0.0.0", port=5000)
    # Run the Flask application
