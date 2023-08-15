from typing import List, Type

from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session

from backend.src.infrastructure.database.entity.entity import CommentEntity
from backend.src.infrastructure.database.repositories.contracts.comment_repository_interface import CommentsRepository


class CommentsRepositoryImpl(CommentsRepository):
    def __init__(self, engine: Engine):
        self.engine = engine

    def get_all_comments(self) -> List[Type[CommentEntity]]:
        with Session(self.engine) as session:
            return session.query(CommentEntity).all()

    def get_comment_by_id(self, comment_id: int) -> Type[CommentEntity] | None:
        with Session(self.engine) as session:
            return session.query(CommentEntity).filter(CommentEntity.id == comment_id).first()

    def get_comment_by_user_id(self, user_id) -> List[Type[CommentEntity]] | None:
        with Session(self.engine) as session:
            return session.query(CommentEntity).filter(CommentEntity.user_id == user_id).all()

    def get_comment_by_project_id(self, project_id) -> List[Type[CommentEntity]] | None:
        with Session(self.engine) as session:
            return session.query(CommentEntity).filter(CommentEntity.project_id == project_id).all()

    def add_comment(self, comment_data: CommentEntity) -> CommentEntity:
        with Session(self.engine) as session:
            session.merge(comment_data)
            session.commit()
        return comment_data

    def update_comment(self, comment_data: CommentEntity) -> Type[CommentEntity] | None:
        with Session(self.engine) as session:
            session.query(CommentEntity).filter(CommentEntity.id == comment_data.id).update({
                CommentEntity.project_id: comment_data.project_id,
                CommentEntity.user_id: comment_data.user_id,
                CommentEntity.comment: comment_data.comment,
                CommentEntity.timestamp: comment_data.timestamp,
            }, synchronize_session="fetch")
            session.commit()
            updated: Type[CommentEntity] = self.get_comment_by_id(comment_data.id)
            return updated

    def delete_comment(self, comment_id: int) -> None:
        with Session(self.engine) as session:
            comment = session.query(CommentEntity).filter(CommentEntity.id == comment_id).first()
            session.delete(comment)
            session.commit()
        return "ok"
