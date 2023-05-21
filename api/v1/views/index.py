#!/usr/bin/python3
"""Import app_views and return JSON for a route
"""
from api.v1.views import app_views
from flask import jsonify


@app_views.route('/status', strict_slashes=False)
def status():
    """Return JSON OK status"""
    return jsonify({'status': 'OK'})
