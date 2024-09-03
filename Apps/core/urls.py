from django.urls import path
from Apps.core.views.dashboard.views import DashboardView
from Apps.core.views.driver.views import  DriverListView, DriverCreateView, DriverDeleteView, DriverUpdateView
from Apps.core.views.ticket.views import TicketCreateView, TicketDeleteView, TicketListView, TicketUpdateView
from Apps.core.views.purchase.views import PurchaseCreateView, PurchaseListView, PurchaseDeleteView, PurchaseUpdateView

app_name = 'core'

urlpatterns = [
    # Home
    path('dashboard/', DashboardView.as_view(), name='dashboard'),

    # Ticket
    path('ticket/list/', TicketListView.as_view(), name='ticket_list'),
    path('ticket/add/', TicketCreateView.as_view(), name='ticket_create'),
    path('ticket/update/<int:pk>/', TicketUpdateView.as_view(), name='ticket_update'),
    path('ticket/delete/<int:pk>/', TicketDeleteView.as_view(), name='ticket_delete'),

    # Driver
    path('driver/list/', DriverListView.as_view(), name='driver_list'),
    path('driver/add/', DriverCreateView.as_view(), name='driver_create'),
    path('driver/update/<int:pk>/', DriverUpdateView.as_view(), name='driver_update'),
    path('driver/delete/<int:pk>/', DriverDeleteView.as_view(), name='driver_delete'),

    # Purchase
    path('purchase/list/', PurchaseListView.as_view(), name='purchase_list'),
    path('purchase/add/', PurchaseCreateView.as_view(), name='purchase_create'),
    path('purchase/update/<int:pk>/', PurchaseUpdateView.as_view(), name='purchase_update'),
    path('purchase/delete/<int:pk>/', PurchaseDeleteView.as_view(), name='purchase_delete'),
]
