#!/usr/bin/python3
"""amenities"""

from flask import request, jsonify, abort
from models.amenity import Amenity
from models import storage
from models.amenity import Amenity
from datetime import datetime
import uuid
from api.v1.views import app_views

# Retrieves the list of all Amenity objects
@app.route('/api/v1/amenities', methods=['GET'])
def get_amenities():
    amenities = Amenity.query.all()
    return jsonify([amenity.to_dict() for amenity in amenities])

# Retrieves a Amenity object
@app.route('/api/v1/amenities/<int:amenity_id>', methods=['GET'])
def get_amenity(amenity_id):
    amenity = Amenity.query.get(amenity_id)
    if not amenity:
        abort(404, message="Amenity not found")
    return jsonify(amenity.to_dict())

# Deletes a Amenity object
@app.route('/api/v1/amenities/<int:amenity_id>', methods=['DELETE'])
def delete_amenity(amenity_id):
    amenity = Amenity.query.get(amenity_id)
    if not amenity:
        abort(404, message="Amenity not found")
    amenity.delete()
    return jsonify({}), 200

# Creates a Amenity
@app.route('/api/v1/amenities', methods=['POST'])
def add_amenity():
    data = request.get_json()
    if not data:
        abort(400, message="Not a JSON")
    if 'name' not in data:
        abort(400, message="Missing name")
    amenity = Amenity(name=data['name'])
    amenity.save()
    return jsonify(amenity.to_dict()), 201

# Updates a Amenity object
@app.route('/api/v1/amenities/<int:amenity_id>', methods=['PUT'])
def update_amenity(amenity_id):
    amenity = Amenity.query.get(amenity_id)
    if not amenity:
        abort(404, message="Amenity not found")
    data = request.get_json()
    if not data:
        abort(400, message="Not a JSON")
    for key, value in data.items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(amenity, key, value)
    amenity.save()
    return jsonify(amenity.to_dict())
