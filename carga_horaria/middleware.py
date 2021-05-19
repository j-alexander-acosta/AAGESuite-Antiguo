from django.shortcuts import redirect


def colegio_middleware(get_response):
    def middleware(request):
        is_switcher = '/carga/switch/' in request.path

        if not request.session.get('colegio__pk', None) and not is_switcher and request.path.startswith('/carga') \
                and not request.path.startswith('/carga/switch-periodo') and not request.path.startswith('/carga/assign'):
            return redirect('/carga/switch/')

        response = get_response(request)
        return response
    return middleware
