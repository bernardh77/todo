from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"), # empty "" means to the root or base of the website. resulting it to go to views.home function and return the http response
    path('', views.todo, name='todo'),
    path('todo/', views.todo, name='todo'),
]