from pyramid.csrf import new_csrf_token
from pyramid.response import Response
from pyramid.security import remember, forget
from pyramid.view import view_config, view_defaults

from backend.src.infrastructure.securite.authenticate import authenticate


@view_defaults()
class LoginView:

    def __init__(self, request):
        self.request = request

    @view_config(route_name='login', request_method='POST')
    def login(self):

        login = self.request.POST['login']
        password = self.request.POST['password']
        user = authenticate(login, password)
        if user:
            new_csrf_token(self.request)
            headers = remember(self.request, userid=user.id, max_age=36000)
            response = Response(json={'result': user.id}, headerlist=headers)
            return response

        response = Response(json={'result': 'ng'})
        return response

    @view_config(route_name='logout', request_method='GET')
    def logout(self):
        headers = forget(self.request)

        response = Response(json={'result': 'logout'}, headerlist=headers)
        return response
