from abc import ABC, abstractmethod

from backend.src.infrastructure.database.entity.entity import UserEntity, ProjectEntity


class ManagementRepository(ABC):

    @abstractmethod
    def update_user_with_projects(self, user_data: UserEntity):
        pass

    @abstractmethod
    def update_project_with_users(self, user_data: ProjectEntity):
        pass

    @abstractmethod
    def create_project_with_users(self, user_data: ProjectEntity):
        pass

