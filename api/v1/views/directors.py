#!/usr/bin/python3
""" objects that handles all default RestFul API actions for Directors"""
from models.director import Director
from models import storage
from api.v1.views import app_views
from flask import abort, jsonify, make_response, request
from flasgger.utils import swag_from


@app_views.route('/director', methods=['GET'], strict_slashes=False)
@swag_from('documentation/director/all_director.yml')
def get_directors():
    """
    Retrieves a list of all directors
    """
    all_directors = storage.all(Directors).values()
    list_directors = []
    for director in all_directors:
        list_directors.append(director.to_dict())
    return jsonify(list_directors)


@app_views.route('/directors/<director_id>/', methods=['GET'],
                 strict_slashes=False)
@swag_from('documentation/director/get_director.yml', methods=['GET'])
def get_director(director_id):
    """ Retrieves a director"""
    director = storage.get(Director, director_id)
    if not director:
        abort(404)

    return jsonify(director.to_dict())


@app_views.route('/directors/<director_id>', methods=['DELETE'],
                 strict_slashes=False)
@swag_from('documentation/directors/delete_director.yml', methods=['DELETE'])
def delete_director(director_id):
    """ Deletes a director  Object"""
    director = storage.get(Director, director_id)

    if not director:
        abort(404)

    storage.delete(director)
    storage.save()

    return make_response(jsonify({}), 200)


@app_views.route('/directors', methods=['POST'], strict_slashes=False)
@swag_from('documentation/director/post_director.yml', methods=['POST'])
def post_director():
    """
    Creates a director
    """
    if not request.get_json():
        abort(400, description="Not a JSON")

    if 'name' not in request.get_json():
        abort(400, description="Missing name")

    data = request.get_json()
    instance = Director(**data)
    instance.save()
    return make_response(jsonify(instance.to_dict()), 201)


@app_views.route('/directors/<director_id>', methods=['PUT'],
                 strict_slashes=False)
@swag_from('documentation/directors/put_director.yml', methods=['PUT'])
def put_director(director_id):
    """
    Updates a director
    """
    if not request.get_json():
        abort(400, description="Not a JSON")

    ignore = ['id', 'created_at', 'updated_at']

    director = storage.get(Director, director_id)

    if not director:
        abort(404)

    data = request.get_json()
    for key, value in data.items():
        if key not in ignore:
            setattr(director, key, value)
    storage.save()
    return make_response(jsonify(director.to_dict()), 200)
