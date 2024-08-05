#!/usr/bin/python3
"""Module that models blueprints."""

from flask import Flask
from models import storage
from api.v1.views import app_views
import os

# Create an instance of Flask
app = Flask(__name__)

# Register the blueprint
app.register_blueprint(app_views)


# Handle teardown_appcontext
@app.teardown_appcontext
def teardown_db(exception):
    """Calls the close method from storage."""
    storage.close()


# Run the Flask server
if __name__ == "__main__":
    host = os.getenv('HBNB_API_HOST', '0.0.0.0')
    port = int(os.getenv('HBNB_API_PORT', 5000))
    app.run(host=host, port=port, threaded=True, debug=True)
