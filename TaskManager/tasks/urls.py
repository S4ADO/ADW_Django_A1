from django.urls import path
from django.conf.urls import include, url

from . import views

urlpatterns = [
    path('', views.signin, name='index'),
    path('tasks/register', views.register, name='register'),
    path('tasks/signin', views.signin, name='signin'),
    path('tasks/home', views.home, name='home'),
    path('tasks/create', views.create, name='create'),
    path('tasks/delete', views.delete, name='delete'),
    path('tasks/logout', views.logout, name='logout'),
]