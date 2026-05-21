from .models import PageView

class TrafficMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # skip admin & static files
        if not request.path.startswith('/admin') and \
           not request.path.startswith('/static'):
            ip = request.META.get('HTTP_X_FORWARDED_FOR', '').split(',')[0] \
                 or request.META.get('REMOTE_ADDR', '0.0.0.0')
            PageView.objects.create(path=request.path, ip_address=ip.strip())

        return self.get_response(request)