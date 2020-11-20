from django.conf.urls import url
from django.urls import path, include
from django.contrib.auth.views import (
										LoginView,
										LogoutView,
										PasswordChangeView,
										PasswordChangeDoneView,
										PasswordResetView, PasswordResetDoneView,
										PasswordResetConfirmView

										)


app_name = 'accounts'


urlpatterns = [
    path('login', LoginView.as_view(template_name='accounts/login.html'), name='login'),
    path('logout', LogoutView.as_view(template_name='accounts/logout.html'), name='logout'),
    path('change-password', PasswordChangeView.as_view(template_name='accounts/change-password.html', success_url = '/'), name='change-password'),
    path('change-password-done', PasswordChangeView.as_view(template_name='accounts/change-password.html'), name='change-password-done'),

    
]

