#!/usr/bin/python3
"""First endpoint for API stats"""
from flask import Flask
from models import storage
from api.v1.views import app_views
from os import getenv

app = Flask(__name__)
app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown_db(close):
    """ Removes current storage"""
    storage.close()

# Setup the host and port to either env values or defaults
host = getenv("HBNB_API_HOST", default="0.0.0.0")
port = getenv("HBNB_API_PORT", default="5000")


if __name__ == "__main__":

    app.run(host=host, port=port, threaded=True)
