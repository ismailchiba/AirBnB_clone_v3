#!/usr/bin/python3

import json
from api.v1.views import app_views
from flask import Flask, request, jsonify
from models.state import State


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def get_states():
    """gets a list of all states"""

@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def get_state_id(state_id):
    """gets a specific state with state_id"""

@app_views.route('/states/<state_id>', methods=['DELETE'], strict_slashes=False)
def delete_state_id(state_id):
    """deletes a specific state with state_id"""

@app_views.route('/states/<state_id>', methods=['POST'], strict_slashes=False)
def create_state_id(state_id):
    """creates a specific state with state_id"""

@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def update_state_id(state_id):
    """updates a specific state with state_id"""