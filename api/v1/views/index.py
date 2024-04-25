import json

from api.v1.views import app_views


@app_views.route('/status')
def status():
    Status = {
        'status': "OK",
    }
    data = json.dumps(Status)
    return data
