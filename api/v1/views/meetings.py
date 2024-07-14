#!/usr/bin/python3
""" objects that handles all default RestFul API actions for meetings """
from models.meetings import Meeting
from models import storage
from api.v1.views import app_views
from flask import abort, jsonify, make_response, request
from flasgger.utils import swag_from


@app_views.route('/meetings/<meeting_id>', methods=['GET'], strict_slashes=False)
@swag_from('documentation/meetings/get_meetings.yml', methods=['GET'])
def get_meeting(meeting_id):
    """
    Retrieves a specific meeting based on id
    """
    meeting = storage.get(Meetings, meeting_id)
    if not meeting:
        abort(404)
    return jsonify(meetings.to_dict())


@app_views.route('/meetings/<meeting_id>', methods=['DELETE'], strict_slashes=False)
@swag_from('documentation/meetings/delete_meeting.yml', methods=['DELETE'])
def delete_meeting(meeting_id):
    """
    Deletes a meeting based on id provided
    """
    meeting = storage.get(Meeting, meeting_id)

    if not meeting:
        abort(404)
    storage.delete(meeting)
    storage.save()

    return make_response(jsonify({}), 200)


@app_views.route('/meetings/<meeting_id>', methods=['POST'],
                 strict_slashes=False)
@swag_from('documentation/meeting/post_meeting.yml', methods=['POST'])
def post_meeting(meeting_id):
    """
    Creates a Meeting
    """
    meeting = storage.get(Meeting, meeting_id)
    if not meeting:
        abort(404)
    if not request.get_json():
        abort(400, description="Not a JSON")
    if 'name' not in request.get_json():
        abort(400, description="Missing name")

    data = request.get_json()
    instance = Meeting(**data)
    instance.meeting_id = meeting.id
    instance.save()
    return make_response(jsonify(instance.to_dict()), 201)


@app_views.route('/meetings/<meeting_id>', methods=['PUT'], strict_slashes=False)
@swag_from('documentation/meeting/put_meeting.yml', methods=['PUT'])
def put_meeting(meeting_id):
    """
    Updates a Meeting
    """
    meeting = storage.get(Meeting, meeting_id)
    if not meeting:
        abort(404)

    if not request.get_json():
        abort(400, description="Not a JSON")

    ignore = ['id', 'department_id', 'created_at', 'updated_at']

    data = request.get_json()
    for key, value in data.items():
        if key not in ignore:
            setattr(meeting, key, value)
    storage.save()
    return make_response(jsonify(meeting.to_dict()), 200)

