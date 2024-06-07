#!/usr/bin/python3
""" A view for User objects that hands all default RESTFul API actions """
from api.v1.views import app_views
from models.user import User
from models import storage
from flask import jsonify, request, abort


@app_views.route('/users', methods=['GET', 'POST'])
def users():
    """Handles the users view"""
    users = storage.all(User).values()

    if request.method == 'GET':
        return jsonify([user.to_dict() for user in users])

    if request.method == 'POST':
        try:
            data = request.get_json()
        except Exception as e:
            abort(400, 'Not a JSON')
        if 'email' not in data.keys():
            abort(400, 'Missing email')
        if 'password' not in data.keys():
            abort(400, 'Missing password')
        user = User(**data)
        storage.new(user)
        storage.save()
        return jsonify(user.to_dict()), 201


@app_views.route('/users/<user_id>', methods=['GET', 'DELETE', 'PUT'])
def user_id(user_id):
    """Handles single user ids"""
    obj = storage.get(User, user_id)

    if request.method == 'GET':
        if not obj:
            abort(404)
        return jsonify(obj.to_dict())

    if request.method == 'DELETE':
        if not obj:
            abort(404)
        storage.delete(obj)
        storage.save()
        return jsonify({}), 200

    if request.method == 'PUT':
        if not obj:
            abort(404)
        try:
            data = request.get_json()
        except Exception as e:
            abort(400, 'Not a JSON')
        skippable = ['id', 'email', 'created_at', 'updated_at']
        for k, v in data.items():
            if k not in skippable:
                setattr(obj, k, v)
        storage.save()
        return jsonify(obj.to_dict()), 200
