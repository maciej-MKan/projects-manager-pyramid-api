import pytest
from datetime import datetime
from unittest.mock import MagicMock
from backend.src.business.models import DTOComment
from backend.src.business.services.comments_service import CommentsService
from backend.src.infrastructure.database.repositories.contracts.comment_repository_interface import CommentsRepository
from backend.src.utils.mappers import (
    comment_entity_dto_mapper,
    comment_dto_entity_mapper,
)


@pytest.fixture
def comments_service():
    comment_repository = MagicMock(spec=CommentsRepository)
    return CommentsService(comment_repository)


def test_get_all_comments(comments_service):
    # GIVEN
    comments = [
        DTOComment(id=1, project=1, author=1, description='Comment 1', date=datetime.now()),
        DTOComment(id=2, project=1, author=2, description='Comment 2', date=datetime.now()),
    ]
    comments_service.comment_repository.get_all_comments.return_value = comments

    # WHEN
    result = comments_service.get_all_comments()

    # THEN
    assert result == comments


def test_get_comments_by_user_id(comments_service):
    # GIVEN
    user_id = 1
    comments = [
        DTOComment(id=1, project=1, author=1, description='Comment 1', date=datetime.now()),
        DTOComment(id=2, project=2, author=1, description='Comment 2', date=datetime.now()),
    ]
    comments_service.comment_repository.get_comment_by_user_id.return_value = comments

    # WHEN
    result = comments_service.get_comments_by_user_id(user_id)

    # THEN
    assert result == comments


def test_get_comments_by_project_id(comments_service):
    # GIVEN
    project_id = 1
    comments = [
        DTOComment(id=1, project=1, author=1, description='Comment 1', date=datetime.now()),
        DTOComment(id=2, project=1, author=2, description='Comment 2', date=datetime.now()),
    ]
    comments_service.comment_repository.get_comment_by_project_id.return_value = comments

    # WHEN
    result = comments_service.get_comments_by_project_id(project_id)

    # THEN
    assert result == comments


def test_get_comment_details(comments_service):
    # GIVEN
    comment_id = 1
    comment = DTOComment(id=comment_id, project=1, author=1, description='Comment 1', date=datetime.now())
    comments_service.comment_repository.get_comment_by_id.return_value = comment

    # WHEN
    result = comments_service.get_comment_details(comment_id)

    # THEN
    assert result == [comment]


def test_get_comment_details_comment_not_found(comments_service):
    # GIVEN
    comment_id = 1
    comments_service.comment_repository.get_comment_by_id.return_value = None

    # WHEN THEN
    with pytest.raises(Exception) as exc:
        comments_service.get_comment_details(comment_id)
    assert str(exc.value) == f"No comment [{comment_id}] found"


def test_create_new_comment(comments_service):
    # GIVEN
    comment = DTOComment(project=1, author=1, description='Comment 1', date=datetime.now())
    comment_entity = comment_dto_entity_mapper(comment)
    comments_service.comment_repository.add_comment.return_value = comment_entity

    # WHEN
    result = comments_service.create_new_comment(comment)

    # THEN
    assert result == comment_entity_dto_mapper(comment_entity)


def test_update_comment(comments_service):
    # GIVEN
    comment_data = DTOComment(id=1, project=1, author=1, description='Comment 1', date=datetime.now())
    comment_entity = comment_dto_entity_mapper(comment_data)
    comments_service.comment_repository.update_comment.return_value = comment_entity

    # WHEN
    result = comments_service.update_comment(comment_data)

    # THEN
    assert result == comment_entity_dto_mapper(comment_entity).get_json()


def test_update_comment_error(comments_service):
    # GIVEN
    comment_data = DTOComment(id=1, project=1, author=1, description='Comment 1', date=datetime.now())
    comments_service.comment_repository.update_comment.return_value = None

    # WHEN THEN
    with pytest.raises(Exception) as exc:
        comments_service.update_comment(comment_data)
    assert str(exc.value) == "update error"


def test_delete_comment(comments_service):
    # GIVEN
    comment_id = 1
    comments_service.comment_repository.delete_comment.return_value = True

    # WHEN
    result = comments_service.delete_comment(comment_id)

    # THEN
    assert result is True
