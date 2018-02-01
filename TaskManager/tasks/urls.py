from django.urls import path
from django.conf.urls import include, url

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('tasks/register', views.register, name='register'),
    path('tasks/signin', views.signin, name='signin'),
    path('tasks/home', views.home, name='home'),
]