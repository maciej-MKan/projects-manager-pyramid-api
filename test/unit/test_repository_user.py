from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from backend.src.infrastructure.database.entity.entity import UserEntity
from backend.src.infrastructure.database.repositories.user_repository import UsersRepositoryImpl


def get_session():
    engine = create_engine('sqlite:///test.db')
    Session = sessionmaker(bind=engine)
    return Session()


def get_engine():
    return create_engine('sqlite:///test.db')


def test_get_all_users():
    with get_session() as session:
        repository = UsersRepositoryImpl(get_engine())

        users = repository.get_all_users()

        assert len(users) == 0

        # Add users to db
        user1 = UserEntity(first_name='John', last_name='Doe', age=30, gender='Male', email='john.doe@example.com',
                           phone_number='123456789')
        user2 = UserEntity(first_name='Jane', last_name='Smith', age=25, gender='Female',
                           email='jane.smith@example.com', phone_number='987654321')
        session.add(user1)
        session.add(user2)
        session.commit()

        users = repository.get_all_users()

        assert len(users) == 2
        assert users[0].first_name == 'John'
        assert users[1].first_name == 'Jane'


def test_get_user_by_id():
    with get_session() as session:
        repository = UsersRepositoryImpl(get_engine())

        user = UserEntity(first_name='John', last_name='Doe', age=30, gender='Male', email='john.doe@example.com',
                          phone_number='123456789')
        session.add(user)
        session.commit()

        user_id = user.id

        user_from_db = repository.get_user_by_id(user_id)

        assert user_from_db is not None
        assert user_from_db.first_name == 'John'
        assert user_from_db.last_name == 'Doe'
        assert user_from_db.age == 30
        assert user_from_db.gender == 'Male'
        assert user_from_db.email == 'john.doe@example.com'
        assert user_from_db.phone_number == '123456789'


def test_add_user():
    with get_session() as session:
        repository = UsersRepositoryImpl(get_engine())

        user = UserEntity(first_name='John', last_name='Doe', age=30, gender='Male', email='john.doe@example.com',
                          phone_number='123456789')

        added_user = repository.add_user(user)

        assert added_user is not None
        assert added_user.first_name == 'John'
        assert added_user.last_name == 'Doe'
        assert added_user.age == 30
        assert added_user.gender == 'Male'
        assert added_user.email == 'john.doe@example.com'
        assert added_user.phone_number == '123456789'


def test_update_user():
    with get_session() as session:
        repository = UsersRepositoryImpl(get_engine())

        user = UserEntity(first_name='John', last_name='Doe', age=30, gender='Male', email='john.doe@example.com',
                          phone_number='123456789')
        session.add(user)
        session.commit()

        user.first_name = 'Updated John'
        user.last_name = 'Updated Doe'
        user.age = 35
        user.gender = 'Female'
        user.email = 'updated.john.doe@example.com'
        user.phone_number = '987654321'

        updated_user = repository.update_user(user)

        assert updated_user is not None
        assert updated_user.first_name == 'Updated John'
        assert updated_user.last_name == 'Updated Doe'
        assert updated_user.age == 35
        assert updated_user.gender == 'Female'
        assert updated_user.email == 'updated.john.doe@example.com'
        assert updated_user.phone_number == '987654321'


def test_delete_user():
    with get_session() as session:
        repository = UsersRepositoryImpl(get_engine())

        user = UserEntity(first_name='John', last_name='Doe', age=30, gender='Male', email='john.doe@example.com',
                          phone_number='123456789')
        session.add(user)
        session.commit()

        user_id = user.id

        deleted_user = repository.delete_user(user_id)

        assert deleted_user == 'ok'
        assert repository.get_user_by_id(user_id) is None


def test_login_user():
    with get_session() as session:
        repository = UsersRepositoryImpl(get_engine())

        user = UserEntity(first_name='John', last_name='Doe', age=30, gender='Male', email='john.doe@example.com',
                          phone_number='123456789', password='password')
        session.add(user)
        session.commit()

        # Try fail login
        login_data = {
            'login': 'john.doe@example.com',
            'password': 'password'
        }
        logged_in_user = repository.login_user(login_data)

        assert logged_in_user is not None
        assert logged_in_user.first_name == 'John'
        assert logged_in_user.last_name == 'Doe'
        assert logged_in_user.age == 30
        assert logged_in_user.gender == 'Male'
        assert logged_in_user.email == 'john.doe@example.com'
        assert logged_in_user.phone_number == '123456789'

        # Try fail login
        login_data = {
            'login': 'john.doe@example.com',
            'password': 'wrong_password'
        }
        logged_in_user = repository.login_user(login_data)

        assert logged_in_user is None
