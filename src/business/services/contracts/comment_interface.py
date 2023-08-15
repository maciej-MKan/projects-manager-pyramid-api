from abc import ABC, abstractmethod


class Comments(ABC):

    @abstractmethod
    def get_all_comments(self):
        pass

    @abstractmethod
    def get_comment_details(self, comment_id):
        pass

    @abstractmethod
    def create_new_comment(self, comment_data):
        pass

    @abstractmethod
    def update_comment(self, new_comment_data):
        pass

    @abstractmethod
    def delete_comment(self, comment_id):
        pass

    @abstractmethod
    def get_comments_by_user_id(self, user_id):
        pass

    @abstractmethod
    def get_comments_by_project_id(self, project_id):
        pass
