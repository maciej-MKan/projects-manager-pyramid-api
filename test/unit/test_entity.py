from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from backend.src.infrastructure.database.entity.entity import ProjectEntity, UserEntity, CommentEntity, Base

# SQLAlchemy engine init
engine = create_engine('sqlite:///test.db')
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base.metadata.create_all(bind=engine)


def get_session():
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()


def test_project_entity_relationships():
    # given
    with get_session() as session:
        user1 = UserEntity(first_name='John', last_name='Doe', email='john.doe@example.com')
        user2 = UserEntity(first_name='Jane', last_name='Smith', email='jane.smith@example.com')
        session.add(user1)
        session.add(user2)
        session.commit()

        project = ProjectEntity(name='Test Project', start_date=0, end_date=1, status='active')
        project.users = [user1, user2]
        session.add(project)
        session.commit()

        comment = CommentEntity(project_id=project.id, user_id=user1.id, comment='Test comment', timestamp=1234567890)
        session.add(comment)
        session.commit()

        # Select db
        project_from_db = session.query(ProjectEntity).first()

        # Check relation
        assert len(project_from_db.users) == 2
        assert project_from_db.users[0] == user1
        assert project_from_db.users[1] == user2
        assert len(project_from_db.comments) == 1
        assert project_from_db.comments[0] == comment
        assert project_from_db.comments[0].user == user1
        assert project_from_db.comments[0].project == project

        # Check relation
        user1_from_db = session.query(UserEntity).filter(UserEntity.id == user1.id).first()
        user2_from_db = session.query(UserEntity).filter(UserEntity.id == user2.id).first()
        assert len(user1_from_db.projects) == 1
        assert len(user2_from_db.projects) == 1
        assert user1_from_db.projects[0] == project
        assert user2_from_db.projects[0] == project

        # Check relation
        comment_from_db = session.query(CommentEntity).first()
        assert comment_from_db.user == user1
        assert comment_from_db.project == project


def test_user_entity_relationships():
    # given
    with get_session() as session:
        project1 = ProjectEntity(name='Project 1', start_date=0, end_date=1, status='active')
        project2 = ProjectEntity(name='Project 2', start_date=0, end_date=1, status='active')
        session.add(project1)
        session.add(project2)
        session.commit()

        user = UserEntity(first_name='John', last_name='Doe', email='john.doe@example.com')
        user.projects = [project1, project2]
        session.add(user)
        session.commit()

        # Select DB
        user_from_db = session.query(UserEntity).first()

        # Check relation
        assert len(user_from_db.projects) == 2
        assert user_from_db.projects[0] == project1
        assert user_from_db.projects[1] == project2

        # Check relation
        project1_from_db = session.query(ProjectEntity).filter(ProjectEntity.id == project1.id).first()
        project2_from_db = session.query(ProjectEntity).filter(ProjectEntity.id == project2.id).first()
        assert len(project1_from_db.users) == 1
        assert len(project2_from_db.users) == 1
        assert project1_from_db.users[0] == user
        assert project2_from_db.users[0] == user


def test_comment_entity_relationships():
    # given
    with get_session() as session:
        user = UserEntity(first_name='John', last_name='Doe', email='john.doe@example.com')
        session.add(user)
        session.commit()

        project = ProjectEntity(name='Test Project', start_date=0, end_date=1, status='active')
        session.add(project)
        session.commit()

        comment = CommentEntity(project_id=project.id, user_id=user.id, comment='Test comment', timestamp=1234567890)
        session.add(comment)
        session.commit()

        # Select DB
        comment_from_db = session.query(CommentEntity).first()

        # Check relation
        assert comment_from_db.user == user
        assert comment_from_db.project == project

        # Check relation
        user_from_db = session.query(UserEntity).filter(UserEntity.id == user.id).first()
        assert len(user_from_db.comments) == 1
        assert user_from_db.comments[0] == comment

        # Check relation
        project_from_db = session.query(ProjectEntity).filter(ProjectEntity.id == project.id).first()
        assert len(project_from_db.comments) == 1
        assert project_from_db.comments[0] == comment
