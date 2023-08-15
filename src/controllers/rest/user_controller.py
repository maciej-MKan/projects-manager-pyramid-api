import json

from pydantic import parse_obj_as
from pyramid.response import Response
from pyramid.view import view_config, view_defaults

from backend.src.business.models.DTOProject import Project
from backend.src.business.models.DTOUser import User
from backend.src.business.services.contracts.user_interface import Users
from backend.src.controllers.exceptions.exceptions_view import ArgumentFailure
from backend.src.infrastructure.configuration.application_configuration import ApplicationConfiguration


@view_defaults(is_authenticated=True)
class UserController:

    def __init__(self, request):
        self.users_service: Users | None = ApplicationConfiguration().get_user_service()
        self.request = request

    @view_config(route_name='users', request_method="GET")
    def get_all_users(self) -> Response:
        users = [user.get_json() for user in self.users_service.get_all_users()]
        response = Response(json=users)
        return response

    @view_config(route_name='user_by_id', request_method="GET")
    def get_user(self) -> Response:
        user_id = None
        try:
            user_id = self.request.GET['user_id']
            user = self.users_service.get_user_details(user_id)
            response = Response(json=user)
            return response
        except AttributeError:
            raise ArgumentFailure(f"No user {user_id} found ")

    @view_config(route_name='create_user', request_method="POST")
    def add_user(self):
        if self.request.json_body.get('projects'):
            raise Exception("Can't add user with projects")
        user_data: dict = self.request.json_body
        result: User = self.users_service.create_new_user(parse_obj_as(User, user_data))
        response = Response(json=result.get_json())
        return response

    @view_config(route_name='update_user', request_method="PUT")
    def update_user(self):
        user_data: dict = self.request.json_body
        user: User = parse_obj_as(User, user_data)
        update_user_result = self.users_service.update_user(user)
        response = Response(json=update_user_result.get_json())
        return response

    @view_config(route_name='delete_user', request_method="DELETE")
    def delete_user_by_id(self):
        user_id = self.request.GET['user_id']
        result = self.users_service.delete_user(user_id)
        response = Response(json=json.dumps(result))
        return response

    # def includeme(self, config):
    #     config.add_view(self.get_all_users)
