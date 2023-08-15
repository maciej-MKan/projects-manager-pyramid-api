from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from backend.src.infrastructure.database.entity.entity import UserEntity, ProjectEntity
from backend.src.infrastructure.database.repositories.comment_repository import CommentsRepositoryImpl
from backend.src.infrastructure.database.repositories.project_repository import ProjectsRepositoryImpl
from backend.src.infrastructure.database.repositories.relation_management_repository import ManagementRepositoryImpl
from backend.src.infrastructure.database.repositories.user_repository import UsersRepositoryImpl


def get_session():
    engine = create_engine('sqlite:///test.db')
    Session = sessionmaker(bind=engine)
    return Session()


def get_engine():
    return create_engine('sqlite:///test.db')


def test_update_user_with_projects():
    with get_session() as session:
        user_repository = UsersRepositoryImpl(get_engine())
        project_repository = ProjectsRepositoryImpl(get_engine())
        comment_repository = CommentsRepositoryImpl(get_engine())

        repository = ManagementRepositoryImpl(get_engine(), user_repository, project_repository, comment_repository)

        # Add user
        user = UserEntity(first_name='John', last_name='Doe', age=30, gender='Male', email='john.doe@example.com',
                          phone_number='123456789')
        user_repository.add_user(user)

        # Add project
        project1 = ProjectEntity(name='Project 1', description='Description 1', start_date='2023-01-01',
                                 end_date='2023-01-31', status='Active')
        project2 = ProjectEntity(name='Project 2', description='Description 2', start_date='2023-02-01',
                                 end_date='2023-02-28', status='Inactive')
        project_repository.add_project(project1)
        project_repository.add_project(project2)

        # Bind user project
        user.projects = [project1, project2]

        # Update DB
        updated_user = repository.update_user_with_projects(user)

        assert updated_user is not None
        assert updated_user.first_name == 'John'
        assert updated_user.last_name == 'Doe'
        assert updated_user.age == 30
        assert updated_user.gender == 'Male'
        assert updated_user.email == 'john.doe@example.com'
        assert updated_user.phone_number == '123456789'
        assert len(updated_user.projects) == 2
        assert updated_user.projects[0].name == 'Project 1'
        assert updated_user.projects[1].name == 'Project 2'


def test_create_project_with_users():
    with get_session() as session:
        user_repository = UsersRepositoryImpl(get_engine())
        project_repository = ProjectsRepositoryImpl(get_engine())
        comment_repository = CommentsRepositoryImpl(get_engine())

        repository = ManagementRepositoryImpl(get_engine(), user_repository, project_repository, comment_repository)

        # Add users
        user1 = UserEntity(first_name='John', last_name='Doe', age=30, gender='Male', email='john.doe@example.com',
                           phone_number='123456789')
        user2 = UserEntity(first_name='Jane', last_name='Smith', age=25, gender='Female',
                           email='jane.smith@example.com', phone_number='987654321')
        user_repository.add_user(user1)
        user_repository.add_user(user2)

        # Create project with users
        project = ProjectEntity(name='Project 1', description='Description 1', start_date='2023-01-01',
                                end_date='2023-01-31', status='Active')
        project.users = [user1, user2]
        created_project = repository.create_project_with_users(project)

        assert created_project is not None
        assert created_project.name == 'Project 1'
        assert created_project.description == 'Description 1'
        assert created_project.start_date == '2023-01-01'
        assert created_project.end_date == '2023-01-31'
        assert created_project.status == 'Active'
        assert len(created_project.users) == 2
        assert created_project.users[0].first_name == 'John'
        assert created_project.users[1].first_name == 'Jane'


def test_update_project_with_users():
    with get_session() as session:
        user_repository = UsersRepositoryImpl(get_engine())
        project_repository = ProjectsRepositoryImpl(get_engine())
        comment_repository = CommentsRepositoryImpl(get_engine())

        repository = ManagementRepositoryImpl(get_engine(), user_repository, project_repository, comment_repository)

        # Add users
        user1 = UserEntity(first_name='John', last_name='Doe', age=30, gender='Male', email='john.doe@example.com',
                           phone_number='123456789')
        user2 = UserEntity(first_name='Jane', last_name='Smith', age=25, gender='Female',
                           email='jane.smith@example.com', phone_number='987654321')
        user_repository.add_user(user1)
        user_repository.add_user(user2)

        # Add project
        project = ProjectEntity(name='Project 1', description='Description 1', start_date='2023-01-01',
                                end_date='2023-01-31', status='Active')
        project_repository.add_project(project)

        # Bind user project
        project.users = [user1, user2]

        # Update DB
        updated_project = repository.update_project_with_users(project)

        assert updated_project is not None
        assert updated_project.name == 'Project 1'
        assert updated_project.description == 'Description 1'
        assert updated_project.start_date == '2023-01-01'
        assert updated_project.end_date == '2023-01-31'
        assert updated_project.status == 'Active'
        assert len(updated_project.users) == 2
        assert updated_project.users[0].first_name == 'John'
        assert updated_project.users[1].first_name == 'Jane'
