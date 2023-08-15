import json
from datetime import datetime
from unittest.mock import MagicMock

from backend.src.controllers.rest.project_controller import ProjectController
from pyramid.response import Response
from pyramid.testing import DummyRequest

from backend.src.business.models.DTOProject import Project
from backend.src.business.models.DTOUser import User
from backend.src.business.services.contracts.project_interface import Projects


def create_dummy_request(json_body=None, query_string=None):
    request = DummyRequest()
    request.json_body = json_body if json_body else {}
    request.GET = query_string if query_string else {}
    return request


def test_get_all_projects():
    # given
    projects = [
        Project(id=1, name='Project 1', users=[], date=datetime.now()),
        Project(id=2, name='Project 2', users=[], date=datetime.now()),
    ]
    projects_service = MagicMock(spec=Projects)
    projects_service.get_all_projects.return_value = projects
    controller = ProjectController(create_dummy_request())
    controller.projects_service = projects_service

    # when
    response = controller.get_all_projects()

    # then
    assert isinstance(response, Response)
    assert response.json == [project.get_json() for project in projects]


def test_get_projects_by_user_id():
    # given
    user_id = 1
    projects = [
        Project(id=1, name='Project 1', users=[], date=datetime.now()),
        Project(id=2, name='Project 2', users=[], date=datetime.now()),
    ]
    projects_service = MagicMock(spec=Projects)
    projects_service.get_projects_by_user_id.return_value = projects
    controller = ProjectController(create_dummy_request(query_string={'user_id': user_id}))
    controller.projects_service = projects_service

    # when
    response = controller.get_projects_by_user_id()

    # then
    assert isinstance(response, Response)
    assert response.json == [project.get_json() for project in projects]


def test_get_project_by_id():
    # given
    project_id = 1
    project = Project(id=project_id, name='Project 1', users=[], date=datetime.now())
    projects_service = MagicMock(spec=Projects)
    projects_service.get_project_details.return_value = [project]
    controller = ProjectController(create_dummy_request(query_string={'project_id': project_id}))
    controller.projects_service = projects_service

    # when
    response = controller.get_project_by_id()

    # then
    assert isinstance(response, Response)
    assert response.json == project.get_json()


def test_update_project():
    # given
    project_data = {
        'id': 1,
        'name': 'Updated Project',
        'users': [{'id': 1, 'name': 'User 1'}, {'id': 2, 'name': 'User 2'}],
        'date': datetime.now().isoformat()
    }
    project = Project(**project_data)
    users = [User(**user) for user in project_data['users']]
    project.users = users
    projects_service = MagicMock(spec=Projects)
    projects_service.update_project.return_value = project_data
    controller = ProjectController(create_dummy_request(json_body=project_data))
    controller.projects_service = projects_service

    # when
    response = controller.update_project()

    # then
    assert isinstance(response, Response)
    assert response.json == project_data


def test_add_project():
    # given
    project_data = {
        'id': 1,
        'name': 'New Project',
        'users': [{'id': 1, 'name': 'User 1'}, {'id': 2, 'name': 'User 2'}],
        'date': datetime.now().isoformat()
    }
    project = Project(**project_data)
    users = [User(**user) for user in project_data['users']]
    project.users = users
    projects_service = MagicMock(spec=Projects)
    projects_service.create_new_project.return_value = project
    controller = ProjectController(create_dummy_request(json_body=project_data))
    controller.projects_service = projects_service

    # when
    response = controller.add_project()

    # then
    assert isinstance(response, Response)
    assert response.json == project.get_json()


def test_delete_project_by_id():
    # given
    project_id = 1
    projects_service = MagicMock(spec=Projects)
    projects_service.delete_project.return_value = True
    controller = ProjectController(create_dummy_request(query_string={'project_id': project_id}))
    controller.projects_service = projects_service

    # when
    response = controller.delete_project_by_id()

    # then
    assert isinstance(response, Response)
    assert response.json == json.dumps(True)