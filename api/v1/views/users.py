#!/usr/bin/python3
""" RESTFul API - State """

from api.v1.views import app_views
from flask import Flask
from models import storage
from models.user import User
from flask import jsonify, request, abort


@app_views.route('/users/', methods=['GET'], strict_slashes=False)
def retrieve_list_all_users():
    """ Retrieves the list of all User objects: GET /api/v1/users """
    if request.method == 'GET':
        list_all_storage = []
        for us in storage.all(User).values():
            list_all_storage.append(us.to_dict())
        return jsonify(list_all_storage)


@app_views.route('/users/<user_id>', methods=['GET'], strict_slashes=False)
def retrieve_one_user(user_id):
    """ Retrieves a User object: GET /api/v1/users/<state_id> """
    if request.method == 'GET':
        if storage.get(User, user_id) is not None:
            return jsonify(storage.get(User, user_id).to_dict())
        abort(404)


@app_views.route('/users/<user_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_one_user(user_id):
    """ Deletes a State object:: DELETE /api/v1/states/<state_id> """
    if request.method == 'DELETE':
        if storage.get(User, user_id) is not None:
            storage.delete(storage.get(User, user_id))
            storage.save()
            return jsonify({}), 200
        abort(404)


@app_views.route('/users/', methods=['POST'], strict_slashes=False)
def create_new_user():
    """ Creates a User: POST /api/v1/users """
    if request.method == 'POST':
        req_type = request.headers.get('Content-Type')
        if req_type != 'application/json':
            return jsonify('Not a JSON'), 400
        dict_req_name = request.get_json()
        if 'email' not in dict_req_name:
            return jsonify('Missing email'), 400
        if 'password' not in dict_req_name:
            return jsonify('Missing password'), 400
        new_obj_User = User(**dict_req_name)
        new_obj_User.save()
        return jsonify(new_obj_User.to_dict()), 201


@app_views.route('/users/<user_id>', methods=['PUT'], strict_slashes=False)
def update_user(user_id):
    """ Updates a State object: PUT /api/v1/states/<state_id> """
    if request.method == 'PUT':
        req_type = request.headers.get('Content-Type')
        if req_type != 'application/json':
            return jsonify('Not a JSON'), 400
        dict_req = request.get_json()
        if storage.get(User, user_id) is not None:
            if 'password' in dict_req:
                storage.get(User, user_id).password = dict_req['password']
            if 'first_name' in dict_req:
                storage.get(User, user_id).first_name = dict_req['first_name']
            if 'last_name' in dict_req:
                storage.get(User, user_id).last_name = dict_req['last_name']
            storage.get(User, user_id).save()
            return jsonify(storage.get(User, user_id).to_dict()), 200
        abort(404)
