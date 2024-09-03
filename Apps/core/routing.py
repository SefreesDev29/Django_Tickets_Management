from django.urls import path
from Apps.core.consumers.dashboard.consumers import DashboardConsumer

websocket_urlpatterns = [
    path('ws/dashboard/', DashboardConsumer.as_asgi()), 
]