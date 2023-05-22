#!/usr/bin/python3
"""New view for Place objects"""
from api.v1.views import app_views
from flask import abort, request, make_response, jsonify
from models import storage
from models.city import City
from models.place import Place


@app_views.route('/cities/<string:city_id>/places', strict_slashes=False)
def places(city_id):
    """Retrieve list of all Place objects"""
    result = []
    obj = storage.get(City, city_id)
    if obj is None:
        abort(404)
    for place in obj.places:
        result.append(place.to_dict())
    return (jsonify(result))


@app_views.route('/places/<string:citybplace>', strict_slashes=False)
def place(pace_id):
    """Retrieve a Place object"""
    obj = storage.get(Place, place_id)
    if obj:
        return obj.to_dict()
    else:
        abort(404)


@app_views.route('/places/<string:place_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_place(palce_id):
    """Delete a Place object"""
    obj = storage.get(Place, place_id)
    if obj:
        obj.delete()
        storage.save()
        return ({}, 200)
    else:
        abort(404)


@app_views.route('/cities/<string:city_id>/places', methods=['POST'],
                 strict_slashes=False)
def post_place(city_id):
    """Post a Place object"""
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
