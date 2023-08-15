from backend.src.business.models import DTOUser
from backend.src.business.services.users_service import UsersService
from backend.src.infrastructure.database.entity.entity import UserEntity
from backend.src.infrastructure.database.repositories.contracts.relation_management_repository_interface import \
    ManagementRepository
from backend.src.infrastructure.database.repositories.contracts.user_repository_interface import UsersRepository


class TestUsersService:

    def test_get_all_users(self, mocker):
        # given
        user_entity = UserEntity(name='John', age=25)
        mocker.patch.object(UsersRepository, 'get_all_users', return_value=[user_entity])
        users_service = UsersService(UsersRepository(), ManagementRepository())

        # when
        result = users_service.get_all_users()

        # then
        assert len(result) == 1
        assert result[0].name == 'John'
        assert result[0].age == 25

    def test_get_user_details(self, mocker):
        # given
        user_id = 1
        user_entity = UserEntity(name='John', age=25)
        mocker.patch.object(UsersRepository, 'get_user_by_id', return_value=user_entity)
        users_service = UsersService(UsersRepository(), ManagementRepository())

        # when
        result = users_service.get_user_details(user_id)

        # then
        assert result['name'] == 'John'
        assert result['age'] == 25

    def test_create_new_user(self, mocker):
        # given
        user = DTOUser(name='John', age=25)
        user_entity = UserEntity(name='John', age=25)
        mocker.patch.object(UsersRepository, 'add_user', return_value=user_entity)
        users_service = UsersService(UsersRepository(), ManagementRepository())

        # when
        result = users_service.create_new_user(user)

        # then
        assert result.name == 'John'
        assert result.age == 25

    def test_update_user(self, mocker):
        # given
        new_user_data = DTOUser(name='John', age=30)
        new_user_entity = UserEntity(name='John', age=30)
        mocker.patch.object(UsersRepository, 'update_user', return_value=new_user_entity)
        users_service = UsersService(UsersRepository(), ManagementRepository())

        # when
        result = users_service.update_user(new_user_data)

        # then
        assert result.name == 'John'
        assert result.age == 30

    def test_delete_user(self, mocker):
        # given
        user_id = 1
        user_entity = UserEntity(name='John', age=25)
        mocker.patch.object(UsersRepository, 'delete_user', return_value=user_entity)
        users_service = UsersService(UsersRepository(), ManagementRepository())

        # when
        result = users_service.delete_user(user_id)

        # then
        assert result.name == 'John'
        assert result.age == 25

    def test_login_user(self, mocker):
        # given
        email = 'john@example.com'
        password = 'password'
        mocker.patch.object(UsersRepository, 'login_user', return_value=True)
        users_service = UsersService(UsersRepository(), ManagementRepository())

        # when
        result = users_service.login_user(email, password)

        # then
        assert result is True
