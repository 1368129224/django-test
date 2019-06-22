from django.urls import path
from django.contrib.auth import views as auth_views
from . import views


app_name = 'account'
urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name='account/login.html'), name='alogin'),
    path('logout/', auth_views.LogoutView.as_view(template_name='account/logout.html'), name='alogout'),
    path('register/', views.register, name='aregister'),
    path('change-password/', auth_views.PasswordChangeView.as_view(template_name='account/password_change_form.html'), name='password_change'),
    path('change-password-done/', auth_views.PasswordChangeDoneView.as_view(template_name='account/password_change_done.html'), name='password_change_done'),
    path('password-reset',
         auth_views.PasswordResetView.as_view(
             template_name='account/password_reset_form.html',
             email_template_name='account/password_reset_email.html',
         ),
         name='password_reset',
         ),
    path('password-reset-done',
         auth_views.PasswordResetDoneView.as_view(
             template_name='account/password_reset_done.html',
         ),
         name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(
             template_name="account/password_reset_confirm.html",
             success_url='/account/password-reset-complete',
         ),
         name="password_reset_confirm"),
    path('password-reset-complete',
         auth_views.PasswordResetCompleteView.as_view(
             template_name='account/password_reset_conplete.html',
         ),
         name='password_reset_complete'),
    path('my-info/', views.myself, name='my_info')
]