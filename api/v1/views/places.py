#!/usr/bin/python3
"""New view for Place objects"""
from api.v1.views import app_views
from flask import abort, request, make_response, jsonify
from models import storage
from models.city import City
from models.place import Place
from models.user import User


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


@app_views.route('/places/<string:place_id>', strict_slashes=False)
def place(place_id):
    """Retrieve a Place object"""
    obj = storage.get(Place, place_id)
    if obj:
        return obj.to_dict()
    else:
        abort(404)


@app_views.route('/places/<string:place_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_place(place_id):
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
    elif 'user_id' not in request.get_json():
        return (make_response(jsonify({'error': 'Missing user_id'}), 400))
    elif 'name' not in request.get_json():
        return (make_response(jsonify({'error': 'Missing name'}), 400))
    else:
        city_obj = storage.get(City, city_id)
        user_obj = storage.get(User, request.get_json()['user_id'])
        if not city_obj:
            abort(404)
        elif not user_obj:
            abort(404)
        options = request.get_json()
        options['city_id'] = city_id
        place = Place(**options)
        place.save()
        return (place.to_dict(), 201)


@app_views.route('/places/<string:place_id>', methods=['PUT'],
                 strict_slashes=False)
def update_place(place_id):
    """Update a Place object"""
    obj = storage.get(Place, place_id)
    if not request.get_json():
        return (make_response(jsonify({'error': 'Not a JSON'}), 400))
    elif obj is None:
        abort(404)
    else:
        for key, val in request.get_json().items():
            if key not in ['id', 'user_id', 'city_id', 'created_at',
                           'updated_at']:
                setattr(obj, key, val)
        obj.save()
        return (obj.to_dict(), 200)
