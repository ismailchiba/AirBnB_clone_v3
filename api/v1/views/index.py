from api.v1.views import app_views, jsonify
from flask import Flask

app = Flask(__name__)

@app_views.route('/status')
def status():
    """ get status"""
    stats = {"status":"OK"}
    return jsonify(stats)
    