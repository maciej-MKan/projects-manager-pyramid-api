from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from backend.src.infrastructure.database.entity.entity import ProjectEntity
from backend.src.infrastructure.database.repositories.project_repository import ProjectsRepositoryImpl


def get_session():
    engine = create_engine('sqlite:///test.db')
    Session = sessionmaker(bind=engine)
    return Session()


def get_engine():
    return create_engine('sqlite:///test.db')


def test_get_all_projects():
    with get_session() as session:
        repository = ProjectsRepositoryImpl(get_engine())

        projects = repository.get_all_projects()

        assert len(projects) == 0

        # Dodanie kilku projektów do bazy danych
        project1 = ProjectEntity(name='Project 1', description='Description 1', start_date=1234567890,
                                 end_date=9876543210, status='Active', user_id=1)
        project2 = ProjectEntity(name='Project 2', description='Description 2', start_date=1234567890,
                                 end_date=9876543210, status='Active', user_id=2)
        session.add(project1)
        session.add(project2)
        session.commit()

        projects = repository.get_all_projects()

        assert len(projects) == 2
        assert projects[0].name == 'Project 1'
        assert projects[1].name == 'Project 2'


def test_get_project_by_id():
    with get_session() as session:
        repository = ProjectsRepositoryImpl(get_engine())

        project = ProjectEntity(name='Test Project', description='Test Description', start_date=1234567890,
                                end_date=9876543210, status='Active', user_id=1)
        session.add(project)
        session.commit()

        project_id = project.id

        project_from_db = repository.get_project_by_id(project_id)

        assert project_from_db is not None
        assert project_from_db.name == 'Test Project'
        assert project_from_db.description == 'Test Description'
        assert project_from_db.start_date == 1234567890
        assert project_from_db.end_date == 9876543210
        assert project_from_db.status == 'Active'
        assert project_from_db.user_id == 1


def test_get_project_by_user_id():
    with get_session() as session:
        repository = ProjectsRepositoryImpl(get_engine())

        project1 = ProjectEntity(name='Project 1', description='Description 1', start_date=1234567890,
                                 end_date=9876543210, status='Active', user_id=1)
        project2 = ProjectEntity(name='Project 2', description='Description 2', start_date=1234567890,
                                 end_date=9876543210, status='Active', user_id=1)
        project3 = ProjectEntity(name='Project 3', description='Description 3', start_date=1234567890,
                                 end_date=9876543210, status='Active', user_id=2)
        session.add_all([project1, project2, project3])
        session.commit()

        projects_for_user1 = repository.get_project_by_user_id(1)
        projects_for_user2 = repository.get_project_by_user_id(2)

        assert len(projects_for_user1) == 2
        assert len(projects_for_user2) == 1


def test_add_project():
    with get_session() as session:
        repository = ProjectsRepositoryImpl(get_engine())

        project = ProjectEntity(name='New Project', description='New Description', start_date=1234567890,
                                end_date=9876543210, status='Active', user_id=1)

        added_project = repository.add_project(project)

        assert added_project is not None
        assert added_project.name == 'New Project'
        assert added_project.description == 'New Description'
        assert added_project.start_date == 1234567890
        assert added_project.end_date == 9876543210
        assert added_project.status == 'Active'
        assert added_project.user_id == 1


def test_update_project():
    with get_session() as session:
        repository = ProjectsRepositoryImpl(get_engine())

        project = ProjectEntity(name='Old Project', description='Old Description', start_date=1234567890,
                                end_date=9876543210, status='Active', user_id=1)
        session.add(project)
        session.commit()

        project.name = 'Updated Project'
        project.description = 'Updated Description'
        project.start_date = 9876543210
        project.end_date = 1234567890
        project.status = 'Inactive'
        project.user_id = 2

        updated_project = repository.update_project(project)

        assert updated_project is not None
        assert updated_project.name == 'Updated Project'
        assert updated_project.description == 'Updated Description'
        assert updated_project.start_date == 9876543210
        assert updated_project.end_date == 1234567890
        assert updated_project.status == 'Inactive'
        assert updated_project.user_id == 2


def test_delete_project():
    with get_session() as session:
        repository = ProjectsRepositoryImpl(get_engine())

        project = ProjectEntity(name='Project to delete', description='Description to delete', start_date=1234567890,
                                end_date=9876543210, status='Active', user_id=1)
        session.add(project)
        session.commit()

        project_id = project.id

        deleted_project = repository.delete_project(project_id)

        assert deleted_project == 'ok'
        assert repository.get_project_by_id(project_id) is None
