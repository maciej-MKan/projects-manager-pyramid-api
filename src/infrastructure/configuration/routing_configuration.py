from pyramid import renderers
from pyramid.config import Configurator

from backend.src.controllers.exceptions.exceptions_view import failed_validation, failed_argument
from backend.src.controllers.rest import user_controller, comment_controller, project_controller
from backend.src.controllers.securite import login


def get_routing(config: Configurator):
    json_renderer = renderers.JSON()

    config.scan(project_controller)
    config.scan(comment_controller)
    config.scan(user_controller)
    config.scan(login)

    config.add_renderer("json", json_renderer)
    config.add_route('projects', '/projects')
    config.add_route('project_by_id', '/project')
    config.add_route('create_project', '/project/new')
    config.add_route('update_project', '/project/update')
    config.add_route('delete_project', '/project/delete')
    config.add_route('projects_from_user', '/user/self_projects')

    config.add_route('users', '/users')
    config.add_route('user_by_id', '/user')
    config.add_route('create_user', '/user/new')
    config.add_route('update_user', '/user/update')
    config.add_route('delete_user', '/user/delete')

    config.add_route('comments', '/comments')
    config.add_route('comment_by_id', '/comment')
    config.add_route('create_comment', '/comment/new')
    config.add_route('update_comment', '/comment/update')
    config.add_route('delete_comment', '/comment/delete')
    config.add_route('user_comments', '/comment/by_user')
    config.add_route('project_comments', '/comment/by_project')

    config.add_route('login', '/login')
    config.add_route('logout', '/logout')

    # config.add_exception_view(failed_validation)
