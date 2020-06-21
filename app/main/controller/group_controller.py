from http import HTTPStatus

from flask import request
from flask_restx import Resource
from werkzeug.exceptions import BadRequest

from ..model.user import User
from ..service.auth_helper import get_logged_in_user
from ..service.group_service import (create_group, delete_group, get_a_group,
                                     get_all_groups, update_group)
from ..util.decorator import token_required
from ..util.dto import AuthDto, GroupDto

api = GroupDto.api
group = GroupDto.group
group_write = GroupDto.group_write
group_post_parser = GroupDto.group_post_parser
group_patch_parser = GroupDto.group_patch_parser
group_write_ret = GroupDto.group_write_ret


@api.route('/<uuid_group>')
@api.response(HTTPStatus.NOT_FOUND, 'Group not found')
class Group(Resource):
    """ Group Resource """

    @api.doc('Export a group', security='jwt')
    @api.marshal_with(group_write_ret)
    @token_required
    def get(self, uuid_group):
        """ Export a group """
        group = get_a_group(uuid_group)
        if group:
            return dict(
                group=group,
            ), HTTPStatus.OK
        else:
            return dict(
                error='Group not found'
            ), HTTPStatus.NOT_FOUND

    @api.doc('Delete a group', security='jwt')
    @token_required
    def delete(self, uuid_group):
        """ Delete a group """
        return delete_group(uuid_group, request.user._uuid)

    @api.doc('Update a group', security='jwt')
    @api.expect(group_write, validate=True)
    @api.response(HTTPStatus.BAD_REQUEST, 'Empty body / Unknown arguments')
    @api.marshal_with(group_write_ret)
    @token_required
    def patch(self, uuid_group):
        """ Update a group """
        if not request.json:
            return dict(
                error="Empty body"
            ), HTTPStatus.BAD_REQUEST

        try:
            data = group_patch_parser.parse_args(strict=True)
        except BadRequest:
            return dict(
                error="Unknown arguments"
            ), HTTPStatus.BAD_REQUEST
        else:
            return update_group(data, uuid_group, request.user._uuid)


@api.route('/')
class GroupList(Resource):
    """ Group List Resource """

    @api.doc('Create a new group', security='jwt')
    @api.expect(group_write)
    @api.response(HTTPStatus.BAD_REQUEST, 'Empty body / Unknown arguments')
    @api.marshal_with(group_write_ret)
    @token_required
    def post(self):
        """ Create a new group """
        if not request.json:
            return dict(
                error="Empty body"
            ), HTTPStatus.BAD_REQUEST

        try:
            data = group_post_parser.parse_args(strict=True)
        except BadRequest:
            return dict(
                error="Unknown arguments"
            ), HTTPStatus.BAD_REQUEST
        else:
            return create_group(data, request.user._uuid)

    @api.doc('Returns all the groups', security='jwt')
    @api.marshal_list_with(group)
    @token_required
    def get(self):
        """ Return all groups """
        return get_all_groups()
