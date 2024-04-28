
from model.engine import db_storage, file_storage
from api.v1.views import app_views
from flask import Flask
from app.app_views import app_views

app = Flask(__name__)


class db_storage:
    """ define class storage """
    def __init__(self):
    """ initialize storage """
        pass

    def close(self):
        """ performs any neccesarily cleanup """
        pass

storage = db_storage()
""" An instance of storage class """

@app.teardown_appcontext
def teardown_storage(exception=None):
    """ Call the close method of storage instance """
    storage.close()


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, threaded=True)
