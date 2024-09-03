from django.urls import path

from Apps.security.views.dashboard.views import DashboardCreateOrUpdateView
from Apps.security.views.accessuser.views import AccessUserListView,AccessUserDeleteView
from Apps.security.views.auditdriver.views import AuditDriverListView
from Apps.security.views.auditpurchase.views import AuditPurchaseListView

app_name = 'security'

urlpatterns = [
    # Config Dashboard
    path('dashboard/update/', DashboardCreateOrUpdateView.as_view(), name='config_dashboard'),

    # Access Users
    path('access/list/', AccessUserListView.as_view(), name='accessuser_list'),
    path('access/delete/<int:pk>/', AccessUserDeleteView.as_view(), name='accessuser_delete'),

    # Audit Drivers
    path('driver/list/', AuditDriverListView.as_view(), name='audit_driver_list'),

    # Audit Purchases
    path('purchase/list/', AuditPurchaseListView.as_view(), name='audit_purchase_list'),
]
