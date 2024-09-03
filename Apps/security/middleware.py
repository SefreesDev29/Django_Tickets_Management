from datetime import timedelta
from django.utils import timezone
from django.conf import settings

class ResetSessionTimeoutMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        session_expiry = request.session.get('_session_expiry')

        if session_expiry and session_expiry < timezone.now():
            request.session.flush()  
        else:
            request.session['_session_expiry'] = timezone.now() + timedelta(seconds=settings.SESSION_COOKIE_AGE)

        response = self.get_response(request)
        return response

class GroupSessionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            groups = request.user.groups.all()
            if groups.exists() and 'group' not in request.session:
                request.session['group'] = groups[0]

        response = self.get_response(request)
        return response