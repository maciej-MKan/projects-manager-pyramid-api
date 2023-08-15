from abc import ABC, abstractmethod


class Projects(ABC):

    @abstractmethod
    def get_all_projects(self):
        pass

    @abstractmethod
    def get_project_details(self, project_id):
        pass

    @abstractmethod
    def create_new_project(self, project_data):
        pass

    @abstractmethod
    def update_project(self, new_project_data):
        pass

    @abstractmethod
    def delete_project(self, project_id):
        pass

    @abstractmethod
    def get_projects_by_user_id(self, user_id):
        pass
