from backend.src.business.models import DTOComment
from backend.src.business.services.contracts.comment_interface import Comments
from backend.src.infrastructure.database.repositories.contracts.comment_repository_interface import CommentsRepository
from backend.src.utils.mappers import *


def map_comments_list(comment_entity):
    comment_list: list[DTOComment] = []
    for entity in comment_entity:
        comment_list.append(comment_entity_dto_mapper(entity))
    print(comment_list)
    return comment_list


class CommentsService(Comments):

    def __init__(self, comment_repository: CommentsRepository):
        self.comment_repository = comment_repository

    def get_all_comments(self):
        comment_entity = self.comment_repository.get_all_comments()
        return map_comments_list(comment_entity)

    def get_comments_by_user_id(self, user_id):
        comment_entity: list[CommentEntity] | None = self.comment_repository.get_comment_by_user_id(user_id)
        return map_comments_list(comment_entity)

    def get_comments_by_project_id(self, user_id):
        comment_entity: list[CommentEntity] | None = self.comment_repository.get_comment_by_project_id(user_id)
        return map_comments_list(comment_entity)

    def get_comment_details(self, comment_id: int):
        comment_entity: list[CommentEntity] | None = self.comment_repository.get_comment_by_id(comment_id)
        if comment_entity:
            return map_comments_list(comment_entity)
        raise Exception(f"No comment [{comment_id}] found")

    def create_new_comment(self, comment: DTOComment):
        comment_entity = comment_dto_entity_mapper(comment)
        new_comment = self.comment_repository.add_comment(comment_entity)
        return comment_entity_dto_mapper(new_comment)

    def update_comment(self, new_comment_data: DTOComment):
        comment_entity = comment_dto_entity_mapper(new_comment_data)
        new_comment = self.comment_repository.update_comment(comment_entity)
        if new_comment:
            return comment_entity_dto_mapper(new_comment).get_json()
        raise Exception("update error")

    def delete_comment(self, comment_id):
        result = self.comment_repository.delete_comment(comment_id)
        return result
