#!/usr/bin/python3
''' Let's create an Amenity view'''

from flask import Flask , abort , request
from api.v1.views import app_views
from os import name
from models.amenity import Amenity


app = Flask(__name__)

@app.route('/api/v1/amenities', methods=['GET'])
def get_amenities():
    """
    Retrieves the list of all Amenity objects.
    """
    amenities = Amenity.all()
    return jsonify([amenity.to_dict() for amenity in amenities])

@app.route('/api/v1/amenities/<amenity_id>', methods=['GET'])
def get_amenity_by_id(amenity_id):
    """
    Retrieves an Amenity object by its ID.
    """
    amenity = Amenity.find(amenity_id)
    if not amenity:
        abort(404)
    return jsonify(amenity.to_dict()), 200

@app.route('/api/v1/amenities/<amenity_id>', methods=['DELETE'])
def delete_amenity(amenity_id):
    """
    Deletes an Amenity object by its ID.
    """
    amenity = Amenity.find(amenity_id)
    if not amenity:
        abort(404)
    amenity.delete()
    return jsonify({}), 200

@app.route('/api/v1/amenities', methods=['POST'])
def create_amenity():
    """
    Creates a new Amenity object.
    """
    if not request.is_json:
        abort(400, {'error': 'Not a JSON'})
    data = request.get_json()
    if 'name' not in data:
        abort(400, {'error': 'Missing name'})
    amenity = Amenity(name=data['name'])
    amenity.save()
    return jsonify(amenity.to_dict()), 201

@app.route('/api/v1/amenities/<amenity_id>', methods=['PUT'])
def update_amenity(amenity_id):
    """
    Updates an Amenity object by its ID.
    """
    if not request.is_json:
        abort(400, {'error': 'Not a JSON'})
    data = request.get_json()
    amenity = Amenity.find(amenity_id)
    if not amenity:
        abort(404)
    ignore_keys = ['id', 'created_at', 'updated_at']
    for key, value in data.items():
        if key not in ignore_keys:
            setattr(amenity, key, value)
    amenity.save()
    return jsonify(amenity.to_dict()), 200

