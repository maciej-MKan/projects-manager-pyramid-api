import pytest
from datetime import datetime
from unittest.mock import MagicMock
from backend.src.business.models import DTOProject
from backend.src.business.services.projects_service import ProjectsService
from backend.src.infrastructure.database.repositories.contracts.project_repository_interface import ProjectsRepository
from backend.src.infrastructure.database.repositories.contracts.relation_management_repository_interface import (
    ManagementRepository
)
from backend.src.utils.mappers import (
    project_entity_dto_mapper,
    project_dto_entity_mapper,
)


@pytest.fixture
def projects_service():
    project_repository = MagicMock(spec=ProjectsRepository)
    management_repository = MagicMock(spec=ManagementRepository)
    return ProjectsService(project_repository, management_repository)


def test_get_all_projects(projects_service):
    # given
    projects = [
        DTOProject(id=1, name='Project 1', description='Description 1', start_date=datetime.now(),
                   end_date=datetime.now(), status='NEW', author=1, users=[]),
        DTOProject(id=2, name='Project 2', description='Description 2', start_date=datetime.now(),
                   end_date=datetime.now(), status='IN_PROGRESS', author=2, users=[]),
    ]
    projects_service.project_repository.get_all_projects.return_value = projects

    # when
    result = projects_service.get_all_projects()

    # then
    assert result == projects


def test_get_projects_by_user_id(projects_service):
    # given
    user_id = 1
    projects = [
        DTOProject(id=1, name='Project 1', description='Description 1', start_date=datetime.now(),
                   end_date=datetime.now(), status='NEW', author=1, users=[]),
        DTOProject(id=2, name='Project 2', description='Description 2', start_date=datetime.now(),
                   end_date=datetime.now(), status='IN_PROGRESS', author=2, users=[]),
    ]
    projects_service.project_repository.get_project_by_user_id.return_value = projects

    # when
    result = projects_service.get_projects_by_user_id(user_id)

    # then
    assert result == projects


def test_get_project_details(projects_service):
    # given
    project_id = 1
    project = DTOProject(id=project_id, name='Project 1', description='Description 1', start_date=datetime.now(),
                         end_date=datetime.now(), status='NEW', author=1, users=[])
    projects_service.project_repository.get_project_by_id.return_value = project

    # when
    result = projects_service.get_project_details(project_id)

    # then
    assert result == project


def test_create_new_project(projects_service):
    # given
    project = DTOProject(name='Project 1', description='Description 1', start_date=datetime.now(),
                         end_date=datetime.now(), status='NEW', author=1, users=[])
    project_entity = project_dto_entity_mapper(project)
    new_project_entity = project_entity
    projects_service.management_repository.create_project_with_users.return_value = new_project_entity

    # when
    result = projects_service.create_new_project(project)

    # then
    assert result == project_entity_dto_mapper(new_project_entity)


def test_update_project(projects_service):
    # given
    project = DTOProject(id=1, name='Project 1', description='Description 1', start_date=datetime.now(),
                         end_date=datetime.now(), status='NEW', author=1, users=[])
    new_project_data = DTOProject(id=1, name='Updated Project 1', description='Updated Description 1',
                                  start_date=datetime.now(), end_date=datetime.now(), status='IN_PROGRESS',
                                  author=1, users=[])
    project_entity = project_dto_entity_mapper(new_project_data)
    projects_service.management_repository.update_project_with_users.return_value = project_entity

    # when
    result = projects_service.update_project(new_project_data)

    # then
    assert result == project_entity_dto_mapper(project_entity).get_json()


def test_delete_project(projects_service):
    # given
    project_id = 1
    projects_service.project_repository.delete_project.return_value = True

    # when
    result = projects_service.delete_project(project_id)

    # then
    assert result is True
