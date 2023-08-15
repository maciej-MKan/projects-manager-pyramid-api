from backend.src.business.models import DTOUser
from backend.src.business.services.contracts.user_interface import Users
from backend.src.infrastructure.database.repositories.contracts.relation_management_repository_interface import \
    ManagementRepository
from backend.src.infrastructure.database.repositories.contracts.user_repository_interface import UsersRepository
from backend.src.utils.mappers import *


class UsersService(Users):

    def __init__(self, user_repository: UsersRepository, management_repository: ManagementRepository):
        self.user_repository = user_repository
        self.management_repository = management_repository

    def get_all_users(self):
        user_entity = self.user_repository.get_all_users()
        user_list: list[DTOUser] = []

        for entity in user_entity:
            user_list.append(user_entity_dto_mapper(entity))
        print(user_list)
        return user_list

    def get_user_details(self, user_id: int):
        return user_entity_dto_mapper(self.user_repository.get_user_by_id(user_id)).get_json()

    def create_new_user(self, user: DTOUser):
        user_entity = user_dto_entity_mapper(user)
        # user_entity.projects = []
        new_user = self.user_repository.add_user(user_entity)
        return user_entity_dto_mapper(new_user)

    def update_user(self, new_user_data: DTOUser) -> User:
        new_user_entity = user_dto_entity_mapper(new_user_data)
        result = self.user_repository.update_user(new_user_entity)
        return user_entity_dto_mapper(result)

    def delete_user(self, user_id) -> User:
        result = self.user_repository.delete_user(user_id)
        return result

    def login_user(self, email: str, password: str):
        data = {"login": email, "password": password}
        return self.user_repository.login_user(data)

