import os

from pyramid.response import Response


def simple_tween_factory(handler, registry):
    def simple_tween(request):
        if request.method == 'OPTIONS':
            response = Response()
            response.headers['Access-Control-Allow-Origin'] = os.environ['FRONT_SERVER']
            response.headers['Access-Control-Allow-Credentials'] = 'true'
            response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE'
            response.headers['Access-Control-Allow-Headers'] = '*'
            return response

        return handler(request)

    return simple_tween
