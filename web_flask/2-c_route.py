#!/usr/bin/python3

"""
script that starts Flask web app
    listen on 0.0.0.0, port 5000
    routes: /:         display "Hello HBNB!"
            /hbnb:     display "HBNB"
            /c/<text>: display "C" + text (replace underscores with space)
"""

from flask import Flask
app = Flask(__name__)
app.url_map.strict_slashes = False


@app.route('/')
def hello_hbnb():
    """script that display text"""
    return "Hello HBNB!"


@app.route('/hbnb')
def hbnb():
    """script that display text"""
    return "HBNB"


@app.route('/c/<text>')
def c_text(text):
    """script that display custom text given"""
    return "C {}".format(text.replace('_', ' '))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
