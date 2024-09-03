from datetime import datetime, timedelta
from types import SimpleNamespace

from django.conf import settings

from Apps.security.models import Dashboard

def site_settings(request):
    year = datetime.now() + timedelta(days=365*2)
    dashboard = Dashboard.objects.first()

    if not dashboard:
        dashboard = SimpleNamespace(name='Sistema Web')

        def get_logo(self):
            return '{}{}'.format(settings.STATIC_URL, 'img/logoweb.png')
        
        def get_background(self):
            return '{}{}'.format(settings.STATIC_URL, 'img/Centro.jpg')
        
        dashboard.get_logo = get_logo.__get__(dashboard)
        dashboard.get_background = get_background.__get__(dashboard)

    return {
        "year" : year.strftime('%Y'),
        "dashboard": dashboard,
    }