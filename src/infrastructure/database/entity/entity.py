from typing import List

from sqlalchemy import ForeignKey
from sqlalchemy.orm import DeclarativeBase, mapped_column, Mapped, registry
from sqlalchemy.orm import relationship


class Base(DeclarativeBase):
    pass


mapper_registry = registry()


@mapper_registry.mapped
class ProjectUser:
    __tablename__ = 'project_users'

    id: Mapped[int] = mapped_column(primary_key=True)
    project_id: Mapped[int] = mapped_column(ForeignKey('projects.id'))
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))

    user_list: Mapped["UserEntity"] = relationship(
        # back_populates="project_asoc",
        lazy="subquery",
    )
    project_list: Mapped["ProjectEntity"] = relationship(
        # back_populates="user_asoc",
        lazy="subquery",
    )


@mapper_registry.mapped
class ProjectEntity:
    __tablename__ = 'projects'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)
    description: Mapped[str] = mapped_column()
    start_date: Mapped[int] = mapped_column(nullable=False)
    end_date: Mapped[int] = mapped_column(nullable=False)
    status: Mapped[str] = mapped_column(nullable=False)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    users: Mapped[List["UserEntity"]] = relationship(secondary="project_users",
                                                     back_populates="projects",
                                                     lazy="subquery",
                                                     overlaps="user_list,project_list, project_asoc",
                                                     )

    # user_asoc: Mapped[List["ProjectUser"]] = relationship(back_populates="project_list",
    #                                                       lazy="subquery",
    #                                                       overlaps="users"
    #                                                       )
    project_comments: Mapped[List["CommentEntity"]] = relationship(lazy="subquery")


@mapper_registry.mapped
class UserEntity:
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True)
    first_name: Mapped[str] = mapped_column(nullable=False)
    last_name: Mapped[str] = mapped_column(nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
    age: Mapped[int] = mapped_column()
    gender: Mapped[str] = mapped_column()
    email: Mapped[str] = mapped_column(nullable=False, unique=True)
    phone_number: Mapped[str] = mapped_column()
    projects: Mapped[List["ProjectEntity"]] = relationship(secondary="project_users",
                                                           back_populates="users",
                                                           lazy="subquery",
                                                           overlaps="project_list,user_asoc,user_list"
                                                           )

    # project_asoc: Mapped[List["ProjectUser"]] = relationship(back_populates="user_list",
    #                                                          lazy="subquery",
    #                                                          overlaps="projects,users"
    #                                                          )
    user_comments: Mapped[List["CommentEntity"]] = relationship(backref="project_comments")


@mapper_registry.mapped
class CommentEntity:
    __tablename__ = 'project_comments'

    id: Mapped[int] = mapped_column(primary_key=True)
    project_id: Mapped[int] = mapped_column(ForeignKey('projects.id'), nullable=False)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'), nullable=False)
    comment: Mapped[str] = mapped_column(nullable=False)
    timestamp: Mapped[int] = mapped_column(nullable=False)

    project_rel = relationship("ProjectEntity",
                               lazy="subquery",
                               back_populates="project_comments",
                               # backref='projects',
                               # single_parent=True,
                               cascade="all, delete")
    #
    # user_rel = relationship("UserEntity",
    #                         lazy="subquery",
    #                         back_populates="comments",
    #                         single_parent=True,
    #                         cascade="all, delete-orphan", )
