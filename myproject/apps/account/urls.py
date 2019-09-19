"""myproject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from django.contrib.auth import views as auth_views
from . import views

app_name = 'account'
urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name='account/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='account/logout.html'), name='logout'),
    path('register/', views.registerView.as_view(), name='register'),
    path('password-change/', auth_views.PasswordChangeView.as_view(
            template_name='account/password_change_form.html'
            , success_url='/account/password-change-done/'
    ), name='password_change'),
    path('password-change-done/', auth_views.PasswordChangeDoneView.as_view(template_name='account/password_change_done.html')
         , name='password_change_done'),
    path('password-reset/', auth_views.PasswordResetView.as_view(
        template_name='account/password_reset_form.html',
        email_template_name='account/password_reset_email.html',
        success_url='/account/password-reset-done',
    ), name='password_reset'),
    path('password-reset-done', auth_views.PasswordResetDoneView.as_view(template_name='account/password_reset_done.html'), name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name='account/password_reset_confirm.html',
        success_url='/account/password-reset-complete/'
    ), name='password_reset_confirm'),
    path('password-reset-complete/', auth_views.PasswordResetCompleteView.as_view(template_name='account/password_reset_complete.html'), name='password_reset_complete'),
    path('my-info/', views.my_info.as_view(), name='my_info'),
    path('change-info/', views.change_my_info.as_view(), name='change_my_info'),
    path('my-avatar/', views.my_avatar.as_view(), name='my_avatar'),
]

