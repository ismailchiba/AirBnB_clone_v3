#!/usr/bin/python3
from flask import Flask, render_template
import uuid
import logging

app = Flask(__name__)

# Set up logging
logging.basicConfig(level=logging.DEBUG)

@app.route('/0-hbnb/')
def display_hbnb():
    cache_id = uuid.uuid4()
    return render_template('0-hbnb.html', cache_id=cache_id)

if __name__ == "__main__":
    logging.info("Starting Flask application...")
    try:
        app.run(host="0.0.0.0", port=5000, debug=True)
    except Exception as e:
        logging.error("Error occurred: {}".format(e))
