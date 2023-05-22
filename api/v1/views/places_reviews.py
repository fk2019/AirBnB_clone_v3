#!/usr/bin/python3
"""New view for  Review objects"""
from api.v1.views import app_views
from flask import abort, request, make_response, jsonify
from models import storage
from models.place import Place
from models.review import Review
from models.user import User


@app_views.route('/places/<string:place_id>/reviews', strict_slashes=False)
def reviews():
    """Retrieve list of all Review objects"""
    result = []
    obj = storage.all(Place, place_id)
    if obj is None:
        abort(404)
    for rev in obj.reviews:
        result.append(rev.to_dict())
    return (jsonify(result))


@app_views.route('/reviews/<string:review_id>', strict_slashes=False)
def review(review_id):
    """Retrieve a Review object"""
    obj = storage.get(Review, review_id)
    if obj:
        return obj.to_dict()
    else:
        abort(404)


@app_views.route('/reviews/<string:review_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_review(review_id):
    """Delete a Review object"""
    obj = storage.get(Review, review_id)
    if obj:
        obj.delete()
        storage.save()
        return ({}, 200)
    else:
        abort(404)


@app_views.route('/places/<strings:place_id>/reviews', methods=['POST'],
                 strict_slashes=False)
def post_review():
    """Post a Review object"""
    if not request.get_json():
        return (make_response(jsonify({'error': 'Not a JSON'}), 400))
    elif 'user_id' not request.get_json():
        return (make_response(jsonify({'error': 'Missing user_id'}), 400))
    elif 'text' not request.get_json():
        return (make_response(jsonify({'error': 'text'}), 400))
    place_obj = storage.get(Place, place_id)
    user_obj = storage.get(User, user_id)
    if not place_obj or not user_obj:
        abort(404)
    options = request.get_json()
    options['user_id'] = user_id
    review_obj = Review(**options)
    review_obj.save()
    return (review_obj.to_dict(), 201)


@app_views.route('/reviews/<string:review_id>', methods=['PUT'],
                 strict_slashes=False)
def update_review(review_id):
    """Update a Review object"""
    obj = storage.get(Review, review_id)
    if not request.get_json():
        return (make_response(jsonify({'error': 'Not a JSON'}), 400))
    elif obj is None:
        abort(404)
    else:
        for key, val in request.get_json().items():
            if key not in ['id', 'user_id', 'place_id', 'created_at',
                           'updated_at']:
                setattr(obj, key, val)
        obj.save()
        return (obj.to_dict(), 200)
