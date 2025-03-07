from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"), # empty "" means to the root or base of the website. resulting it to go to views.home function and return the http response
    path('todo/', views.todo, name='todo'),
    path('todo/add/', views.add_todo, name='add_todo'),
    path('todo/<int:todo_id>/toggle/', views.toggle_todo, name='toggle_todo'),
    path('todo/<int:todo_id>/delete/', views.delete_todo, name='delete_todo'),
]