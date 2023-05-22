#!/usr/bin/python3
"""New view for Amenity objects"""
from api.v1.views import app_views
from flask import abort, request, make_response, jsonify
from models import storage
from models.amenity import Amenity


@app_views.route('/amenities', strict_slashes=False)
def amenities():
    """Retrieve list of all Amenity objects"""
    result = []
    obj = storage.all(Amenity)
    print(obj)
    if obj is None:
        abort(404)
    for am in obj.values():
        result.append(am.to_dict())
    return (jsonify(result))


@app_views.route('/amenities/<string:amenity_id>', strict_slashes=False)
def amenity(amenity_id):
    """Retrieve a Amenity object"""
    obj = storage.get(Amenity, amenity_id)
    if obj:
        return obj.to_dict()
    else:
        abort(404)


@app_views.route('/amenities/<string:amenity_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_amenity(amenity_id):
    """Delete a Amenity object"""
    obj = storage.get(Amenity, amenity_id)
    if obj:
        obj.delete()
        storage.save()
        return ({}, 200)
    else:
        abort(404)


@app_views.route('/amenities', methods=['POST'],
                 strict_slashes=False)
def post_amenity():
    """Post a Amenity object"""
    if not request.get_json():
        return (make_response(jsonify({'error': 'Not a JSON'}), 400))
    elif 'name' not in request.get_json():
        return (make_response(jsonify({'error': 'Missing name'}), 400))
    else:
        obj = Amenity(**request.get_json())
        if not obj:
            abort(404)
        obj.save()
        return (obj.to_dict(), 201)


@app_views.route('/amenities/<string:amenity_id>', methods=['PUT'],
                 strict_slashes=False)
def update_amenity(amenity_id):
    """Update a Amenity object"""
    obj = storage.get(Amenity, amenity_id)
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
