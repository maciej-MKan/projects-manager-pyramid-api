from pyramid.response import Response
from pyramid.view import exception_view_config


class ValidationFailure(Exception):
    pass


class ArgumentFailure(Exception):
    pass


@exception_view_config(context=ValidationFailure)
def failed_validation(exc, request):
    msg = exc.args[0] if exc.args else ""
    response = Response(json={'error': {'Failed validation': msg}})
    response.status_int = 500
    return response


@exception_view_config(context=ArgumentFailure, renderer="json")
def failed_argument(exc, request):
    msg = exc.args[0] if exc.args else ""
    response = Response(json={'error': {'Incorrect argument': msg}})
    response.status_int = 500
    return response
