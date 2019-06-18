from django.urls import path
from django.contrib.auth import views as auth_views
from . import views


urlpatterns = [
    # path('', views.user_login, name='alogin'),
    path('login/', auth_views.LoginView.as_view(template_name='account/login.html'), name='alogin'),
    path('logout/', auth_views.LogoutView.as_view(template_name='account/logout.html'), name='alogout'),
    path('register/', views.register, name='aregister'),
    path('change-password/', auth_views.PasswordChangeView.as_view(template_name='account/password_change_form.html'), name='password_change'),
    path('change-password-done/', auth_views.PasswordChangeDoneView.as_view(template_name='account/password_change_done.html'), name='password_change_done'),
]