from abc import ABC, abstractmethod

from sqlalchemy.orm import Session

from backend.src.infrastructure.database.entity.entity import UserEntity


class UsersRepository(ABC):

    @abstractmethod
    def get_all_users(self):
        pass

    @abstractmethod
    def get_user_by_id(self, user_id: int):
        pass

    @abstractmethod
    def add_user(self, user_data: UserEntity):
        pass

    @abstractmethod
    def update_user(self, user_data: UserEntity, external_session: Session):
        pass

    @abstractmethod
    def delete_user(self, user_id: int):
        pass

    @abstractmethod
    def login_user(self, data: dict):
        pass
