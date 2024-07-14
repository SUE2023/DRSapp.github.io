#!/usr/bin/python3
""" objects that handles all default RestFul API actions for Staff"""
from models.staff import Staff
from models import storage
from api.v1.views import app_views
from flask import abort, jsonify, make_response, request
from flasgger.utils import swag_from


@app_views.route('/staff', methods=['GET'], strict_slashes=False)
@swag_from('documentation/staff/all_staffs.yml')
def get_staffs():
    """
    Retrieves a list of all staffs
    """
    all_staffs = storage.all(Staffs).values()
    list_staffs = []
    for staff in all_staffs:
        list_staffs.append(staff.to_dict())
    return jsonify(list_staffs)


@app_views.route('/staffs/<staff_id>/', methods=['GET'],
                 strict_slashes=False)
@swag_from('documentation/staff/get_staff.yml', methods=['GET'])
def get_staff(staff_id):
    """ Retrieves a staff """
    staff = storage.get(Staff, staff_id)
    if not staff:
        abort(404)

    return jsonify(staff.to_dict())


@app_views.route('/staffs/<staff_id>', methods=['DELETE'],
                 strict_slashes=False)
@swag_from('documentation/staff/delete_staff.yml', methods=['DELETE'])
def delete_staff(staff_id):
    """ Deletes a staff  Object"""
    staff = storage.get(Staff, staff_id)

    if not staff:
        abort(404)

    storage.delete(staff)
    storage.save()

    return make_response(jsonify({}), 200)


@app_views.route('/staffs', methods=['POST'], strict_slashes=False)
@swag_from('documentation/staff/post_staff.yml', methods=['POST'])
def post_staff():
    """
    Creates a staff
    """
    if not request.get_json():
        abort(400, description="Not a JSON")

    if 'name' not in request.get_json():
        abort(400, description="Missing name")

    data = request.get_json()
    instance = Staff(**data)
    instance.save()
    return make_response(jsonify(instance.to_dict()), 201)


@app_views.route('/staffs/<staff_id>', methods=['PUT'],
                 strict_slashes=False)
@swag_from('documentation/staff/put_staff.yml', methods=['PUT'])
def put_staff(staff_id):
    """
    Updates a staff
    """
    if not request.get_json():
        abort(400, description="Not a JSON")

    ignore = ['id', 'created_at', 'updated_at']

    staff = storage.get(Staff, staff_id)

    if not staff:
        abort(404)

    data = request.get_json()
    for key, value in data.items():
        if key not in ignore:
            setattr(staff, key, value)
    storage.save()
    return make_response(jsonify(staff.to_dict()), 200)
