#!/usr/bin/python3
""" objects that handles all default RestFul API actions for Boards"""
from models.boards import Board
from models import storage
from api.v1.views import app_views
from flask import abort, jsonify, make_response, request
from flasgger.utils import swag_from


@app_views.route('/board', methods=['GET'], strict_slashes=False)
@swag_from('documentation/board/all_board.yml')
def get_boards():
    """
    Retrieves a list of all boards
    """
    all_boards = storage.all(Boards).values()
    list_boards = []
    for board in all_boards:
        list_boards.append(board.to_dict())
    return jsonify(list_boards)


@app_views.route('/boards/<board_id>/', methods=['GET'],
                 strict_slashes=False)
@swag_from('documentation/board/get_board.yml', methods=['GET'])
def get_board(board_id):
    """ Retrieves a board"""
    board = storage.get(Board, board_id)
    if not board:
        abort(404)

    return jsonify(board.to_dict())


@app_views.route('/boards/<board_id>', methods=['DELETE'],
                 strict_slashes=False)
@swag_from('documentation/board/delete_board.yml', methods=['DELETE'])
def delete_board(board_id):
    """ Deletes a board  Object"""
    board = storage.get(Board, board_id)

    if not board:
        abort(404)

    storage.delete(board)
    storage.save()

    return make_response(jsonify({}), 200)


@app_views.route('/boards', methods=['POST'], strict_slashes=False)
@swag_from('documentation/board/post_board.yml', methods=['POST'])
def post_board():
    """
    Creates a board
    """
    if not request.get_json():
        abort(400, description="Not a JSON")

    if 'name' not in request.get_json():
        abort(400, description="Missing name")

    data = request.get_json()
    instance = Board(**data)
    instance.save()
    return make_response(jsonify(instance.to_dict()), 201)


@app_views.route('/boards/<board_id>', methods=['PUT'],
                 strict_slashes=False)
@swag_from('documentation/board/put_board.yml', methods=['PUT'])
def put_board(board_id):
    """
    Updates a board
    """
    if not request.get_json():
        abort(400, description="Not a JSON")

    ignore = ['id', 'created_at', 'updated_at']

    board = storage.get(Board, board_id)

    if not board:
        abort(404)

    data = request.get_json()
    for key, value in data.items():
        if key not in ignore:
            setattr(board, key, value)
    storage.save()
    return make_response(jsonify(board.to_dict()), 200)
