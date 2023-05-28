#!/usr/bin/python3
"""New view for Place objects"""
from api.v1.views import app_views
from flask import abort, request, make_response, jsonify
from models import storage
from models.amenity import Amenity
from models.state import State
from models.city import City
from models.place import Place
from models.user import User
import json


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


@app_views.route('/places_search', methods=['POST'], strict_slashes=False)
def places_search():
    """Retrieve list of all Place objects...better"""
    data = request.get_json()
    all_places = [place for place in storage.all(Place).values()]
    if not json.dumps(data):
        return (make_response(jsonify({'error': 'Not a JSON'}), 400))
    if len(data) == 0:
        res = json.dumps(data)
        if res == '{}':
            for place in all_places:
                review = []
                for r in place.reviews:
                    review.append(r.to_dict())
                place.review = review
            for place in all_places:
                del place.reviews
            return (jsonify([place.to_dict() for place in all_places]))

    states = data.get('states')
    cities = data.get('cities')
    amenities = data.get('amenities')

    places_list = []
    keys = ["states", "cities", "amenities"]
    if len(data) == 1:
        for key in data.keys():
            if len(data[key]) <= 1 and (data[key] == [] or data[key] == [""]):
                return (jsonify([place.to_dict() for place in all_places]))
    if states and len(states) > 0:
        state_objs = [storage.get(State, state_id) for state_id in states]
        places_l = [pl for ob in state_objs if ob for city in ob.cities if
                    city for pl in city.places]
        places_list += [place for place in places_l if
                        place not in places_list]
    if cities and len(cities) > 0:
        city_objs = [storage.get(City, city_id) for city_id in cities]
        places_l = [pl for city in city_objs if city for pl in city.places]
        places_list += [place for place in places_l if
                        place not in places_list]
    if amenities and len(amenities) > 0:
        amenity_objs = [storage.get(Amenity, amenity_id) for
                        amenity_id in amenities]
        new_list = []
        if len(places_list) > 0:
            for pl in places_list:
                for am in amenity_objs:
                    if am in pl.amenities:
                        new_list.append(pl)
        if len(new_list) > 0:
            for place in new_list:
                del place.amenities
            return jsonify([place.to_dict() for place in new_list])
        else:
            for pl in all_places:
                for am in amenity_objs:
                    if am in pl.amenities:
                        del pl.amenities
                        new_list.append(pl)
            return (jsonify([place.to_dict() for place in new_list]))
    places = []
    for place in places_list:
        del place.amenities
        places.append(place.to_dict())
    return (jsonify(places))
