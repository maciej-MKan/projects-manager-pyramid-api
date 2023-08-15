import json

from pydantic import parse_obj_as
from pyramid.response import Response
from pyramid.view import view_config, view_defaults

from backend.src.business.models.DTOProject import Project
from backend.src.business.models.DTOUser import User
from backend.src.business.services.contracts.project_interface import Projects
from backend.src.infrastructure.configuration.application_configuration import ApplicationConfiguration


@view_defaults(is_authenticated=True)
class ProjectController:
    def __init__(self, request):
        self.request = request
        self.projects_service: Projects | None = ApplicationConfiguration().get_project_service()

    @view_config(route_name='projects', request_method="GET")
    def get_all_projects(self) -> Response:
        projects = [project.get_json() for project in self.projects_service.get_all_projects()]
        response = Response(json=projects, status=200)
        print(response)
        return response

    @view_config(route_name='projects_from_user', request_method="GET")
    def get_projects_by_user_id(self) -> Response:
        user_id = self.request.GET['user_id']
        projects = [project.get_json() for project in self.projects_service.get_projects_by_user_id(user_id)]
        response = Response(json=projects)
        return response

    @view_config(route_name='project_by_id', request_method="GET")
    def get_project_by_id(self) -> Response:
        project_id = self.request.GET['project_id']
        project = self.projects_service.get_project_details(project_id)
        response = Response(json=project.get_json())
        return response

    @view_config(route_name='update_project', request_method="PUT")
    def update_project(self):
        project_data: dict = self.request.json_body
        project: Project = parse_obj_as(Project, project_data)
        users = [parse_obj_as(User, user) for user in project.users]
        project.users = users
        project_update_result = self.projects_service.update_project(project)
        response = Response(json=project_update_result)
        return response

    @view_config(route_name='create_project', request_method="POST")
    def add_project(self):
        project_data: dict = self.request.json_body
        project: Project = parse_obj_as(Project, project_data)
        users = [parse_obj_as(User, user) for user in project.users]
        project.users = users
        project_update_result = self.projects_service.create_new_project(project)
        response = Response(json=project_update_result.get_json())
        return response

    @view_config(route_name='delete_project', request_method="DELETE")
    def delete_project_by_id(self):
        project_id = self.request.GET['project_id']
        result = self.projects_service.delete_project(project_id)
        response = Response(json=json.dumps(result))
        return response

    # def includeme(self, config):
    #     config.add_view(self.get_all_projects)
