from backend.src.business.models import DTOProject
from backend.src.business.services.contracts.project_interface import Projects
from backend.src.infrastructure.database.repositories.contracts.project_repository_interface import ProjectsRepository
from backend.src.infrastructure.database.repositories.contracts.relation_management_repository_interface import \
    ManagementRepository
from backend.src.utils.mappers import *


def map_projects_list(project_entity):
    project_list: list[DTOProject] = []
    for entity in project_entity:
        project_list.append(project_entity_dto_mapper(entity))
    print(project_list)
    return project_list


class ProjectsService(Projects):
    def __init__(self, project_repository: ProjectsRepository, management_repository: ManagementRepository):
        self.project_repository = project_repository
        self.management_repository = management_repository

    def get_all_projects(self):
        project_entity = self.project_repository.get_all_projects()
        print("getting all projects")
        return map_projects_list(project_entity)

    def get_projects_by_user_id(self, user_id):
        project_entity: list[ProjectEntity] = self.project_repository.get_project_by_user_id(user_id)
        return map_projects_list(project_entity)

    def get_project_details(self, project_id: int):
        return project_entity_dto_mapper(self.project_repository.get_project_by_id(project_id))

    def create_new_project(self, project: DTOProject):
        project.status = "NEW"
        project_entity = project_dto_entity_mapper(project)
        new_project_entity = self.management_repository.create_project_with_users(project_entity)
        return project_entity_dto_mapper(new_project_entity)

    def update_project(self, new_project_data: DTOProject):
        project_entity = project_dto_entity_mapper(new_project_data)
        new_project = self.management_repository.update_project_with_users(project_entity)
        if new_project:
            return project_entity_dto_mapper(new_project).get_json()
        raise Exception("update error")

    def delete_project(self, project_id):
        result = self.project_repository.delete_project(project_id)
        return result
