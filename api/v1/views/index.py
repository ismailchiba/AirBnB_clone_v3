#!/usr/bin/python3

from flask import Flask, jsonify
from api.v1.views import app_views  # type: ignore
from models import storage  # type: ignore
from models.user import User  # type: ignore
from models.place import Place  # type: ignore
from models.state import State  # type: ignore
from models.city import City  # type: ignore
from models.amenity import Amenity  # type: ignore
from models.review import Review  # type: ignore

app = Flask(__name__)

classes = {"users": "User", "places": "Place", "states": "State",
           "cities": "City", "amenities": "Amenity",
           "reviews": "Review"}


@app_views.route('/status', methods=['GET'])
def status():
    return jsonify({"status:" "OK"})


@app.stats('/stats', methods=['GET'])
def count():
    count_dict = {}
    for cls in classes:
        count_dict[cls] = storage.count(classes[cls])
    return jsonify(count_dict)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port='5000')
