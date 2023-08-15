from ..database.repositories.relation_management_repository import ManagementRepositoryImpl
from ...infrastructure.configuration.database_configuration import DataBaseEngine

from ...business.services.projects_service import ProjectsService
from ...infrastructure.database.repositories.project_repository import ProjectsRepositoryImpl

from ...business.services.users_service import UsersService
from ...infrastructure.database.repositories.user_repository import UsersRepositoryImpl

from ...business.services.comments_service import CommentsService
from ...infrastructure.database.repositories.comment_repository import CommentsRepositoryImpl


class ApplicationConfiguration:
    _configuration = None

    def __init__(self):
        self._project_repository = ProjectsRepositoryImpl(DataBaseEngine())
        self._user_repository = UsersRepositoryImpl(DataBaseEngine())
        self._comment_repository = CommentsRepositoryImpl(DataBaseEngine())
        self._management_repository = ManagementRepositoryImpl(
            DataBaseEngine(),
            self._user_repository,
            self._project_repository,
            self._comment_repository
        )

        self._project_service = ProjectsService(self._project_repository, self._management_repository)
        self._user_service = UsersService(self._user_repository, self._management_repository)
        self._comment_service = CommentsService(self._comment_repository)

    def get_project_service(self):
        return self._project_service

    def get_project_repository(self):
        return self._project_repository

    def get_user_service(self):
        return self._user_service

    def get_user_repository(self):
        return self._user_repository

    def get_comment_service(self):
        return self._comment_service

    def get_comment_repository(self):
        return self._project_repository
