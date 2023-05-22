#!/usr/bin/python3
"""New view for  User objects"""
from api.v1.views import app_views
from flask import abort, request, make_response, jsonify
from models import storage
from models.user import User


@app_views.route('/users', strict_slashes=False)
def users():
    """Retrieve list of all User objects"""
    result = []
    obj = storage.all(User)
    print(obj)
    if obj is None:
        abort(404)
    for am in obj.values():
        result.append(am.to_dict())
    return (jsonify(result))


@app_views.route('/users/<string:user_id>', strict_slashes=False)
def user(user_id):
    """Retrieve a User object"""
    obj = storage.get(User, user_id)
    if obj:
        return obj.to_dict()
    else:
        abort(404)


@app_views.route('/users/<string:user_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_user(user_id):
    """Delete a User object"""
    obj = storage.get(User, user_id)
    if obj:
        obj.delete()
        storage.save()
        return ({}, 200)
    else:
        abort(404)


@app_views.route('/users', methods=['POST'],
                 strict_slashes=False)
def post_user():
    args = ['first_name', 'last_name', 'email', 'password']
    """Post a User object"""
    if not request.get_json():
        return (make_response(jsonify({'error': 'Not a JSON'}), 400))
    for arg in args:
        if arg not in request.get_json():
            return (make_response(jsonify({'error': 'Missing {}'.format(arg)}),
                                  400))
    obj = User(**request.get_json())
    if not obj:
        abort(404)
    obj.save()
    return (obj.to_dict(), 201)


@app_views.route('/users/<string:user_id>', methods=['PUT'],
                 strict_slashes=False)
def update_user(user_id):
    """Update a User object"""
    obj = storage.get(User, user_id)
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
