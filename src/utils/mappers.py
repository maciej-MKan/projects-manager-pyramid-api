from datetime import datetime

from backend.src.business.models.DTOComment import Comment
from backend.src.business.models.DTOProject import Project
from backend.src.business.models.DTOUser import User
from backend.src.infrastructure.database.entity.entity import UserEntity, ProjectEntity, CommentEntity


def project_entity_dto_mapper(entity: ProjectEntity):
    return Project(
        id=entity.id,
        name=entity.name,
        description=entity.description,
        start_date=datetime.fromtimestamp(entity.start_date),
        end_date=datetime.fromtimestamp(entity.end_date),
        status=entity.status,
        author=entity.user_id,
        users=[user_entity_dto_mapper(user) for user in entity.users]
    )


def project_dto_entity_mapper(project_data: Project):
    print(project_data.users)
    if not project_data.users:
        project_data.users = []
    users_ = [user_dto_entity_mapper(user) for user in project_data.users]
    return ProjectEntity(
        id=project_data.id,
        name=project_data.name,
        description=project_data.description,
        start_date=int(project_data.start_date.timestamp()),
        end_date=int(project_data.end_date.timestamp()),
        status=project_data.status,
        user_id=project_data.author,
        users=users_
    )


def user_entity_dto_mapper(entity: UserEntity) -> User:
    return User(
        id=entity.id,
        name=entity.first_name,
        surname=entity.last_name,
        age=entity.age,
        gender=entity.gender,
        email=entity.email,
        phone_number=entity.phone_number,
        # projects=[],
        # projects=[project_entity_dto_mapper(project) for project in entity.projects],
    )


def user_dto_entity_mapper(user_data: User) -> UserEntity:
    # if not user_data.projects:
    #     user_data.projects = []
    # projects_ = [project_dto_entity_mapper(project) for project in user_data.projects]
    print(user_data)
    print(user_data.id)
    return UserEntity(
        id=user_data.id,
        first_name=user_data.name,
        last_name=user_data.surname,
        password=user_data.password,
        age=user_data.age,
        gender=user_data.gender,
        email=user_data.email,
        phone_number=user_data.phone_number,
        # projects=projects_,
    )


def comment_entity_dto_mapper(entity: CommentEntity) -> Comment:
    return Comment(
        id=entity.id,
        project=entity.project_id,
        author=entity.user_id,
        description=entity.comment,
        date=datetime.fromtimestamp(entity.timestamp),
    )


def comment_dto_entity_mapper(comment_data: Comment) -> CommentEntity:
    return CommentEntity(
        id=comment_data.id,
        project_id=comment_data.project,
        user_id=comment_data.author,
        comment=comment_data.description,
        timestamp=int(comment_data.date.timestamp()),
    )
