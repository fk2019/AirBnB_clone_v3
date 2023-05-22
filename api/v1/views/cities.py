#!/usr/bin/python3
"""New view for City objects"""
from api.v1.views import app_views
from flask import abort, request, make_response, jsonify
from models import storage
from models.state import State
from models.city import City


@app_views.route('/states/<string:state_id>/cities', strict_slashes=False)
def cities(state_id):
    """Retrieve list of all City objects"""
    result = []
    obj = storage.get(State, state_id)
    if obj is None:
        abort(404)
    for city in obj.cities:
        result.append(city.to_dict())
    return (jsonify(result))


@app_views.route('/cities/<string:city_id>', strict_slashes=False)
def city(city_id):
    """Retrieve a City object"""
    obj = storage.get(City, city_id)
    if obj:
        return obj.to_dict()
    else:
        abort(404)


@app_views.route('/cities/<string:city_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_city(city_id):
    """Delete a City object"""
    obj = storage.get(City, city_id)
    if obj:
        obj.delete()
        storage.save()
        return ({}, 200)
    else:
        abort(404)


@app_views.route('/states/<string:state_id>/cities', methods=['POST'],
                 strict_slashes=False)
def post_city(state_id):
    """Post a City object"""
    if not request.get_json():
        return (make_response(jsonify({'error': 'Not a JSON'}), 400))
    elif 'name' not in request.get_json():
        return (make_response(jsonify({'error': 'Missing name'}), 400))
    else:
        obj = storage.get(State, state_id)
        if not obj:
            abort(404)
        options = request.get_json()
        options['state_id'] = state_id
        city = City(**options)
        city.save()
        return (city.to_dict(), 201)


@app_views.route('/cities/<string:city_id>', methods=['PUT'],
                 strict_slashes=False)
def update_city(city_id):
    """Update a City object"""
    obj = storage.get(City, city_id)
    if not request.get_json():
        return (make_response(jsonify({'error': 'Not a JSON'}), 400))
    elif obj is None:
        abort(404)
    else:
        for key, val in request.get_json().items():
            if key not in ['id', 'created_at', 'updated_at']:
                setattr(obj, key, val)
        obj.save()
        return (obj.to_dict(), 200)
