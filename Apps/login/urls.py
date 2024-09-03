from django.urls import path

from Apps.login.views import LoginFormView, LogoutRedirectView, ResetPasswordView, ChangePasswordView

urlpatterns = [
    path('', LoginFormView.as_view(), name='login'),
    path('logout/', LogoutRedirectView.as_view(), name='logout'),
    path('reset/password/', ResetPasswordView.as_view(), name='reset_password'),
    path('change/password/<str:token>/', ChangePasswordView.as_view(), name='change_password')
]
