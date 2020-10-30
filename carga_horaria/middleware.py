from django.shortcuts import redirect

def colegio_middleware(get_response):
    def middleware(request):
        is_switcher = '/carga/switch/' in request.path

        if not request.session.get('colegio__pk', None) and not is_switcher and not request.path.startswith('/login') and not request.path.startswith('/admin') and not request.path.startswith('/carga/switch-periodo'):
            return redirect('/carga/switch/')

        response = get_response(request)
        return response
    return middleware
