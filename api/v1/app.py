#!/usr/bin/python3

"""Run Flask app at port 5000"""


from api.v1.views import app_views as AV
from api.v1.views.index import *
from flask import Flask as F, make_response as MR
from models import storage


app = F(__name__)


@app.teardown_appcontenxt
def teardown_appcontenxt(code):
    """ Close storage - Task 3 """
    storage.close()


@app.errorhandler(404)
def handle_404(error):
    """ Render template - Task 3"""
    return MR(jsonify({'error': 'Not found'}), 404)


app.register_blueprint(AV)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, threaded=True)
