from api.v1.views import app_views

@app_views.route('/status')
def status():
    """Status of the api."""
    return {"status": "OK"}
