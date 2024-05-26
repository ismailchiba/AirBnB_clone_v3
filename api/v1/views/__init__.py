#!/usr/bin/python3
""" """
from flask import Blueprint

app_views = Blueprint('app_views', __name__)

@app_views.route('/status', methods=['GET'])
def status():
    return {"status": "OK"}