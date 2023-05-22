#!/usr/bin/python3
"""New view for State objects"""
from api.v1.views import app_views
from flask import abort, request, make_response, jsonify
from models import storage
from models.state import State


@app_views.route('/states', strict_slashes=False)
def states():
    """Retrieve list of all State objects"""
    result = []
    for obj in storage.all(State).values():
        result.append(obj.to_dict())
    return (result)


@app_views.route('/states/<string:state_id>', strict_slashes=False)
def state(state_id):
    """Retrieve a State object"""
    obj = storage.get(State, state_id)
    print(state_id)
    if obj:
        return obj.to_dict()
    else:
        abort(404)


@app_views.route('/states/<string:state_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_state(state_id):
    """Delete a State object"""
    obj = storage.get(State, state_id)
    if obj:
        obj.delete()
        storage.save()
        return ({})
    else:
        abort(404)


@app_views.route('/states', methods=['POST'],
                 strict_slashes=False)
def post_state():
    """Post a State object"""
    if not request.get_json():
        return (make_response(jsonify({'error': 'Not a JSON'}), 400))
    elif 'name' not in request.get_json():
        return (make_response(jsonify({'error': 'Missing name'}), 400))
    else:
        obj = State(**request.get_json())
        obj.save()
        return (obj.to_dict(), 201)


@app_views.route('/states/<string:state_id>', methods=['PUT'],
                 strict_slashes=False)
def update_state(state_id):
    """Update a State object"""
    obj = storage.get(State, state_id)
    if not request.get_json():
        return (make_response(jsonify({'error': 'Not a JSON'}), 400))
    elif obj is None:
        abort(404)
    else:
        for key, val in request.get_json().items():
            if key not in ['id', 'created_at', 'updated_at']:
                setattr(obj, key, val)
        obj.save()
        return (obj.to_dict())
