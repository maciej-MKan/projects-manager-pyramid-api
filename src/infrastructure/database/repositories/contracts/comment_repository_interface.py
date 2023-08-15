from abc import ABC, abstractmethod
from typing import List

from backend.src.business.models.DTOComment import Comment
from backend.src.infrastructure.database.entity.entity import CommentEntity


class CommentsRepository(ABC):

    @abstractmethod
    def get_all_comments(self) -> List[CommentEntity]:
        pass

    @abstractmethod
    def get_comment_by_id(self, comment_id: int) -> CommentEntity | None:
        pass

    @abstractmethod
    def add_comment(self, comment_data: CommentEntity) -> CommentEntity:
        pass

    @abstractmethod
    def update_comment(self, comment_data: CommentEntity) -> CommentEntity | None:
        pass

    @abstractmethod
    def delete_comment(self, comment_id: int) -> CommentEntity | None:
        pass

    @abstractmethod
    def get_comment_by_user_id(self, user_id) -> List[CommentEntity] | None:
        pass

    @abstractmethod
    def get_comment_by_project_id(self, user_id) -> List[CommentEntity] | None:
        pass
