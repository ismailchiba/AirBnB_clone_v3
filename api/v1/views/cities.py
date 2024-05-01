#!/usr/bin/python3
"""API City view."""
from api.v1.views import app_views
from flask import abort, jsonify, request
from models import storage
from models.city import City


@app_views.route("/states/<state_id>/cities", methods=["GET", "POST"])
def cities_by_state(state_id):
    """Defines GET and POST methods for citieS"""
    state = storage.get("State", state_id)
    if state is None:
        abort(404)

    if request.method == "GET":
        return jsonify([city.to_dict() for city in state.cities])

    data = request.get_json(silent=True)
    if data is None:
        return "Not a JSON", 400
    if data.get("name") is None:
        return "Missing name", 400
    data["state_id"] = state_id
    city = City(**data)
    city.save()
    return jsonify(city.to_dict()), 201


@app_views.route("/cities/<city_id>", methods=["GET", "DELETE", "PUT"])
def city_id(city_id):
    """Defines GET, DELETE and PUT methods"""
    city = storage.get("City", city_id)
    if city is None:
        abort(404)

    if request.method == "GET":
        return jsonify(city.to_dict())

    elif request.method == "DELETE":
        city.delete()
        storage.save()
        return jsonify({})

    data = request.get_json(silent=True)
    if data is None:
        return "Not a JSON", 400
    avoid = {"id", "state_id", "created_at", "updated_at"}
    [setattr(city, k, v) for k, v in data.items() if k not in avoid]
    city.save()
    return jsonify(city.to_dict())
