from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from backend.src.infrastructure.database.entity.entity import CommentEntity
from backend.src.infrastructure.database.repositories.comment_repository import CommentsRepositoryImpl


def get_session():
    engine = create_engine('sqlite:///test.db')
    Session = sessionmaker(bind=engine)
    return Session()


def get_engine():
    return create_engine('sqlite:///test.db')


def test_get_all_comments():
    with get_session() as session:
        repository = CommentsRepositoryImpl(get_engine())

        comments = repository.get_all_comments()

        assert len(comments) == 0

        # Add users to db
        comment1 = CommentEntity(comment='Comment 1', project_id=1, user_id=1, timestamp=1234567890)
        comment2 = CommentEntity(comment='Comment 2', project_id=1, user_id=2, timestamp=1234567890)
        session.add(comment1)
        session.add(comment2)
        session.commit()

        comments = repository.get_all_comments()

        assert len(comments) == 2
        assert comments[0].comment == 'Comment 1'
        assert comments[1].comment == 'Comment 2'


def test_get_comment_by_id():
    with get_session() as session:
        repository = CommentsRepositoryImpl(get_engine())

        comment = CommentEntity(comment='Test Comment', project_id=1, user_id=1, timestamp=1234567890)
        session.add(comment)
        session.commit()

        comment_id = comment.id

        comment_from_db = repository.get_comment_by_id(comment_id)

        assert comment_from_db is not None
        assert comment_from_db.comment == 'Test Comment'
        assert comment_from_db.project_id == 1
        assert comment_from_db.user_id == 1
        assert comment_from_db.timestamp == 1234567890


def test_get_comment_by_user_id():
    with get_session() as session:
        repository = CommentsRepositoryImpl(get_engine())

        comment1 = CommentEntity(comment='Comment 1', project_id=1, user_id=1, timestamp=1234567890)
        comment2 = CommentEntity(comment='Comment 2', project_id=2, user_id=1, timestamp=1234567890)
        comment3 = CommentEntity(comment='Comment 3', project_id=3, user_id=2, timestamp=1234567890)
        session.add_all([comment1, comment2, comment3])
        session.commit()

        comments_for_user1 = repository.get_comment_by_user_id(1)
        comments_for_user2 = repository.get_comment_by_user_id(2)

        assert len(comments_for_user1) == 2
        assert len(comments_for_user2) == 1


def test_get_comment_by_project_id():
    with get_session() as session:
        repository = CommentsRepositoryImpl(get_engine())

        comment1 = CommentEntity(comment='Comment 1', project_id=1, user_id=1, timestamp=1234567890)
        comment2 = CommentEntity(comment='Comment 2', project_id=1, user_id=2, timestamp=1234567890)
        comment3 = CommentEntity(comment='Comment 3', project_id=2, user_id=1, timestamp=1234567890)
        session.add_all([comment1, comment2, comment3])
        session.commit()

        comments_for_project1 = repository.get_comment_by_project_id(1)
        comments_for_project2 = repository.get_comment_by_project_id(2)

        assert len(comments_for_project1) == 2
        assert len(comments_for_project2) == 1


def test_add_comment():
    with get_session() as session:
        repository = CommentsRepositoryImpl(get_engine())

        comment = CommentEntity(comment='New Comment', project_id=1, user_id=1, timestamp=1234567890)

        added_comment = repository.add_comment(comment)

        assert added_comment is not None
        assert added_comment.comment == 'New Comment'
        assert added_comment.project_id == 1
        assert added_comment.user_id == 1
        assert added_comment.timestamp == 1234567890


def test_update_comment():
    with get_session() as session:
        repository = CommentsRepositoryImpl(get_engine())

        comment = CommentEntity(comment='Old Comment', project_id=1, user_id=1, timestamp=1234567890)
        session.add(comment)
        session.commit()

        comment.comment = 'Updated Comment'
        comment.timestamp = 9876543210

        updated_comment = repository.update_comment(comment)

        assert updated_comment is not None
        assert updated_comment.comment == 'Updated Comment'
        assert updated_comment.timestamp == 9876543210


def test_delete_comment():
    with get_session() as session:
        repository = CommentsRepositoryImpl(get_engine())

        comment = CommentEntity(comment='Comment to delete', project_id=1, user_id=1, timestamp=1234567890)
        session.add(comment)
        session.commit()

        comment_id = comment.id

        deleted_comment = repository.delete_comment(comment_id)

        assert deleted_comment == 'ok'
        assert repository.get_comment_by_id(comment_id) is None
