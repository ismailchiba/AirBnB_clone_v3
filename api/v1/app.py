""" airbnb api wih flask"""


from flask import Flask
from models import storage
from api.v1.views import app_viwes

app = Flask(__name__)
app.register_blueprint(app_viwes)


@app.teardown_appcontext
def tearodwn_close(exception):
    """close data base"""
    storage.close()

app.route("/status")
def status():
    return jsonify({"status": "ok"})



if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, threaded=True)