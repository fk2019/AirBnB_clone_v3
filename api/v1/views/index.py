#!/usr/bin/python3
"""Import app_views and return JSON for a route
"""
from api.v1.views import app_views
from flask import jsonify
from models import storage

hbnb = {'amenities': 'Amenity', 'cities': 'City',
        'places': 'Place', 'reviews': 'Review',
        'states': 'State', 'users': 'User'
        }


@app_views.route('/status', strict_slashes=False)
def status():
    """Return JSON OK status"""
    return jsonify({'status': 'OK'})


@app_views.route('/stats', strict_slashes=False)
def stats():
    """Return number of each object"""
    result = {}
    for key, value in hbnb.items():
        result[key] = storage.count(value)
    return jsonify(result)
