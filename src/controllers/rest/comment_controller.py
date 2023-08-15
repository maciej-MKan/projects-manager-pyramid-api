import json

from pydantic import parse_obj_as
from pyramid.response import Response
from pyramid.view import view_config, view_defaults

from backend.src.business.models.DTOComment import Comment
from backend.src.business.services.contracts.comment_interface import Comments
from backend.src.infrastructure.configuration.application_configuration import ApplicationConfiguration


@view_defaults(is_authenticated=True)
class CommentController:
    def __init__(self, request):
        self.request = request
        self.comments_service: Comments = ApplicationConfiguration().get_comment_service()

    @view_config(route_name='comments', request_method="GET")
    def get_all_comments(self) -> Response:
        comments = [comment.get_json() for comment in self.comments_service.get_all_comments()]
        response = Response(json=comments)
        return response

    @view_config(route_name='comment_by_id', request_method="GET")
    def get_comment(self) -> Response:
        comment_id = self.request.GET['comment_id']
        comment = self.comments_service.get_comment_details(comment_id)
        response = Response(json=comment.get_json())
        return response

    @view_config(route_name='user_comments', request_method="GET")
    def get_comments_by_user_id(self) -> Response:
        user_id = self.request.GET['user_id']
        comments = [comment.get_json() for comment in self.comments_service.get_comments_by_user_id(user_id)]
        response = Response(json=comments)
        return response

    @view_config(route_name='project_comments', request_method="GET")
    def get_comments_by_project_id(self) -> Response:
        project_id = self.request.GET['project_id']
        comments = [comment.get_json() for comment in self.comments_service.get_comments_by_project_id(project_id)]
        response = Response(json=comments)
        return response

    @view_config(route_name='update_comment', request_method="PUT")
    def update_comment(self):
        comment_data: dict = self.request.json_body
        comment: Comment = parse_obj_as(Comment, comment_data)
        comment_update_result = self.comments_service.update_comment(comment)
        response = Response(json=comment_update_result)
        return response

    @view_config(route_name='create_comment', request_method="POST")
    def add_comment(self):
        comment_data: dict = self.request.json_body
        result = self.comments_service.create_new_comment(parse_obj_as(Comment, comment_data))
        response = Response(json=result.get_json())
        return response

    @view_config(route_name='delete_comment', request_method="DELETE")
    def delete_comment_by_id(self):
        comment_id = self.request.GET['comment_id']
        result = self.comments_service.delete_comment(comment_id)
        response = Response(json=json.dumps(result))
        return response
