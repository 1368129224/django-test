from django.urls import path
from . import views


app_name = 'mytest'
urlpatterns = [
    path('', views.index, name='index')
]