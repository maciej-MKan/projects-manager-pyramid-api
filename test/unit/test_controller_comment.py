import json
from datetime import datetime
from unittest.mock import MagicMock

from backend.src.controllers.rest.comment_controller import CommentController
from pyramid.response import Response
from pyramid.testing import DummyRequest

from backend.src.business.models.DTOComment import Comment
from backend.src.business.services.contracts.comment_interface import Comments


def create_dummy_request(json_body=None, query_string=None):
    request = DummyRequest()
    request.json_body = json_body if json_body else {}
    request.GET = query_string if query_string else {}
    return request


def test_get_all_comments():
    # given
    comments = [
        Comment(id=1, project=1, author=1, description='Comment 1', date=datetime.now()),
        Comment(id=2, project=1, author=2, description='Comment 2', date=datetime.now()),
    ]
    comments_service = MagicMock(spec=Comments)
    comments_service.get_all_comments.return_value = comments
    controller = CommentController(create_dummy_request())
    controller.comments_service = comments_service

    # when
    response = controller.get_all_comments()

    # then
    assert isinstance(response, Response)
    assert response.json == [comment.get_json() for comment in comments]


def test_get_comment():
    # given
    comment_id = 1
    comment = Comment(id=comment_id, project=1, author=1, description='Comment 1', date=datetime.now())
    comments_service = MagicMock(spec=Comments)
    comments_service.get_comment_details.return_value = [comment]
    controller = CommentController(create_dummy_request(query_string={'comment_id': comment_id}))
    controller.comments_service = comments_service

    # when
    response = controller.get_comment()

    # then
    assert isinstance(response, Response)
    assert response.json == comment.get_json()


def test_get_comments_by_user_id():
    # given
    user_id = 1
    comments = [
        Comment(id=1, project=1, author=1, description='Comment 1', date=datetime.now()),
        Comment(id=2, project=2, author=1, description='Comment 2', date=datetime.now()),
    ]
    comments_service = MagicMock(spec=Comments)
    comments_service.get_comments_by_user_id.return_value = comments
    controller = CommentController(create_dummy_request(query_string={'user_id': user_id}))
    controller.comments_service = comments_service

    # when
    response = controller.get_comments_by_user_id()

    # then
    assert isinstance(response, Response)
    assert response.json == [comment.get_json() for comment in comments]


def test_get_comments_by_project_id():
    # given
    project_id = 1
    comments = [
        Comment(id=1, project=1, author=1, description='Comment 1', date=datetime.now()),
        Comment(id=2, project=1, author=2, description='Comment 2', date=datetime.now()),
    ]
    comments_service = MagicMock(spec=Comments)
    comments_service.get_comments_by_project_id.return_value = comments
    controller = CommentController(create_dummy_request(query_string={'project_id': project_id}))
    controller.comments_service = comments_service

    # when
    response = controller.get_comments_by_project_id()

    # then
    assert isinstance(response, Response)
    assert response.json == [comment.get_json() for comment in comments]


def test_update_comment():
    # given
    comment_data = {
        'id': 1,
        'project': 1,
        'author': 1,
        'description': 'Updated Comment',
        'date': datetime.now().isoformat()
    }
    comment = Comment(**comment_data)
    comments_service = MagicMock(spec=Comments)
    comments_service.update_comment.return_value = comment_data
    controller = CommentController(create_dummy_request(json_body=comment_data))
    controller.comments_service = comments_service

    # when
    response = controller.update_comment()

    # then
    assert isinstance(response, Response)
    assert response.json == comment_data


def test_add_comment():
    # given
    comment_data = {
        'id': 1,
        'project': 1,
        'author': 1,
        'description': 'New Comment',
        'date': datetime.now().isoformat()
    }
    comment = Comment(**comment_data)
    comments_service = MagicMock(spec=Comments)
    comments_service.create_new_comment.return_value = comment
    controller = CommentController(create_dummy_request(json_body=comment_data))
    controller.comments_service = comments_service

    # when
    response = controller.add_comment()

    # then
    assert isinstance(response, Response)
    assert response.json == comment.get_json()


def test_delete_comment_by_id():
    # given
    comment_id = 1
    comments_service = MagicMock(spec=Comments)
    comments_service.delete_comment.return_value = True
    controller = CommentController(create_dummy_request(query_string={'comment_id': comment_id}))
    controller.comments_service = comments_service

    # when
    response = controller.delete_comment_by_id()

    # then
    assert isinstance(response, Response)
    assert response.json == json.dumps(True)