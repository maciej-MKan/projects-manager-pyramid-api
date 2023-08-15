import json
from unittest.mock import MagicMock
from pyramid.testing import DummyRequest
from pyramid.response import Response
from backend.src.business.models.DTOUser import User
from backend.src.business.services.contracts.user_interface import Users
from backend.src.infrastructure.configuration.application_configuration import ApplicationConfiguration
from backend.src.controllers.rest.user_controller import UserController


def create_dummy_request(json_body=None, query_string=None):
    request = DummyRequest()
    request.json_body = json_body if json_body else {}
    request.GET = query_string if query_string else {}
    return request


def test_get_all_users():
    # given
    users = [
        User(id=1, name='User 1'),
        User(id=2, name='User 2'),
    ]
    users_service = MagicMock(spec=Users)
    users_service.get_all_users.return_value = users
    controller = UserController(create_dummy_request())
    controller.users_service = users_service

    # when
    response = controller.get_all_users()

    # then
    assert isinstance(response, Response)
    assert response.json == [user.get_json() for user in users]


def test_get_user():
    # given
    user_id = 1
    user = User(id=user_id, name='User 1')
    users_service = MagicMock(spec=Users)
    users_service.get_user_details.return_value = user
    controller = UserController(create_dummy_request(query_string={'user_id': user_id}))
    controller.users_service = users_service

    # when
    response = controller.get_user()

    # then
    assert isinstance(response, Response)
    assert response.json == user.get_json()


def test_get_user_not_found():
    # given
    user_id = 1
    users_service = MagicMock(spec=Users)
    users_service.get_user_details.return_value = None
    controller = UserController(create_dummy_request(query_string={'user_id': user_id}))
    controller.users_service = users_service

    # when i sprawdzenie czy wyjątek jest podniesiony
    try:
        controller.get_user()
        assert False  # Jeżeli brak wyjątku, test nie powinien przejść
    except Exception as e:
        assert str(e) == f"No user {user_id} found"


def test_add_user():
    # given
    user_data = {'id': 1, 'name': 'New User'}
    user = User(**user_data)
    users_service = MagicMock(spec=Users)
    users_service.create_new_user.return_value = user
    controller = UserController(create_dummy_request(json_body=user_data))
    controller.users_service = users_service

    # when
    response = controller.add_user()

    # then
    assert isinstance(response, Response)
    assert response.json == user.get_json()


def test_add_user_with_projects():
    # given
    user_data = {'id': 1, 'name': 'New User', 'projects': [{'id': 1, 'name': 'Project 1'}]}
    users_service = MagicMock(spec=Users)
    controller = UserController(create_dummy_request(json_body=user_data))
    controller.users_service = users_service

    # when i sprawdzenie czy wyjątek jest podniesiony
    try:
        controller.add_user()
        assert False  # Jeżeli brak wyjątku, test nie powinien przejść
    except Exception as e:
        assert str(e) == "Can't add user with projects"


def test_update_user():
    # given
    user_data = {'id': 1, 'name': 'Updated User'}
    user = User(**user_data)
    users_service = MagicMock(spec=Users)
    users_service.update_user.return_value = user
    controller = UserController(create_dummy_request(json_body=user_data))
    controller.users_service = users_service

    # when
    response = controller.update_user()

    # then
    assert isinstance(response, Response)
    assert response.json == user.get_json()


def test_delete_user_by_id():
    # given
    user_id = 1
    users_service = MagicMock(spec=Users)
    users_service.delete_user.return_value = True
    controller = UserController(create_dummy_request(query_string={'user_id': user_id}))
    controller.users_service = users_service

    # when
    response = controller.delete_user_by_id()

    # then
    assert isinstance(response, Response)
    assert response.json == json.dumps(True)