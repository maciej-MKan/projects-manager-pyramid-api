from typing import List, Type

from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session, aliased

from backend.src.infrastructure.database.entity.entity import ProjectEntity, UserEntity, ProjectUser
from backend.src.infrastructure.database.repositories.contracts.project_repository_interface import ProjectsRepository


class ProjectsRepositoryImpl(ProjectsRepository):
    def __init__(self, engine: Engine):
        self.engine = engine

    def get_all_projects(self) -> List[Type[ProjectEntity]]:
        with Session(self.engine) as session:
            return session.query(ProjectEntity).all()

    def get_project_by_id(self, project_id: int) -> Type[ProjectEntity] | ProjectEntity:
        with Session(self.engine) as session:
            return session.query(ProjectEntity).filter(ProjectEntity.id == project_id).first()

    def get_project_by_user_id(self, user_id: int) -> list[Type[ProjectEntity]]:
        with Session(self.engine) as session:
            projects = session.query(ProjectEntity).join(ProjectEntity.users).filter(UserEntity.id == user_id).all()
            return projects

    def add_project(self, project_data: ProjectEntity, session: Session = None) -> ProjectEntity:
        if not session:
            session = Session(self.engine)
            try:
                self.add_project(project_data, session)
                session.commit()
                # session.refresh(project_data)
                return project_data
            except Exception as e:
                session.rollback()
                raise e
            finally:
                session.close()
        project_data.users = []
        session.add(project_data)

        return project_data

    def update_project(self, project_data: ProjectEntity, session: Session = None) -> ProjectEntity:
        if not session:
            session = Session(self.engine)
            try:
                self.update_project(project_data, session)
                session.commit()
                updated: ProjectEntity = self.get_project_by_id(project_data.id)
                return updated
            except Exception as e:
                session.rollback()
                raise e
            finally:
                session.close()

        session.query(ProjectEntity).filter(ProjectEntity.id == project_data.id).update(
            {
                ProjectEntity.name: project_data.name,
                ProjectEntity.description: project_data.description,
                ProjectEntity.start_date: project_data.start_date,
                ProjectEntity.end_date: project_data.end_date,
                ProjectEntity.status: project_data.status,
                ProjectEntity.user_id: project_data.user_id,
            }
        )

        return project_data

    def delete_project(self, project_id: int) -> Type[ProjectEntity] | None:
        with Session(self.engine) as session:
            project = session.query(ProjectEntity).filter(ProjectEntity.id == project_id).first()
            session.delete(project)
            session.commit()
        return "ok"
