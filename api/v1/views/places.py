#!/usr/bin/python3
"""A module that handles places"""

from api.v1.views import app_views
from flask import request, jsonify, abort
from models import storage, place


@app_views.route('/cities/<city_id>/places', methods=['GET'],
                 strict_slashes=False)
def getallplaces(city_id=None):
    """A fn that gets all places"""

    if city_id is None:
        abort(404)

    result = []
    for i in storage.all("Place").values():
        result.append(i.to_dict())

    return jsonify(result)


@app_views.route('/places/<place_id>', methods=['GET'], strict_slashes=False)
def getplaces(place_id=None):
    """A fn that gets a place"""

    store = storage.get("Place", place_id)
    if store is None:
        abort(404)
    else:
        return jsonify(store.to_dict())


@app_views.route('/places/<place_id>', methods=['DELETE'],
                 strict_slashes=False)
def deleteplaces(place_id=None):
    """A fn that deletes a place"""

    store = storage.get("Place", place_id)
    if store is None:
        abort(404)
    else:
        storage.delete(obj)
        storage.save()
        return jsonify({}), 200


@app_views.route('/cities/<city_id>/places', methods=['POST'],
                 strict_slashes=False)
def createplaces(city_id=None):
    """A fn that create a place"""

    checker = set()
    for i in storage.all("City").values():
        finder.add(i.id)
    if city_id not in checker:
        abort(404)

    st = request.get_json(silent=True)
    if st is None:
        abort(400, "Not a JSON")

    user = st.get("user_id")
    if user is None:
        abort(400, "Missing user_id")
    checker = set()

    for i in storage.all("User").values():
        checker.add(i.id)

    if user not in checker:
        abort(404)

    if "name" not in st.keys():
        abort(400, "Missing name")

    st["city_id"] = city_id
    new_s = places.Place(**st)
    storage.new(new_s)
    storage.save()
    return jsonify(new_s.to_dict()), 201


@app_views.route('/places/<place_id>', methods=['PUT'], strict_slashes=False)
def updateplaces(place_id=None):
    """A fn that update a place"""

    obj = storage.get("Place", place_id)
    if obj is None:
        abort(404)

    s = request.get_json(silent=True)
    if s is None:
        abort(400, "Not a JSON")
    else:
        for k, v in s.items():
            if k in ['id', 'created_at', 'updated_at', 'user_id', 'city_id']:
                pass
            else:
                setattr(obj, k, v)
        storage.save()
        res = obj.to_dict()
        return jsonify(res), 200
