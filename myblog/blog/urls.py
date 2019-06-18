from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('article/<int:id>', views.article, name='article')
]