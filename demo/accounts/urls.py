from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from rest_framework.routers import DefaultRouter
from django.views.generic import TemplateView

# Create a router and register our viewsets with it
router = DefaultRouter()
router.register(r'todos', views.TodoViewSet, basename='todo')

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('toggle-theme/', views.toggle_theme, name='toggle_theme'),
    path('password-reset/', views.password_reset_request, name='password_reset'),
    path('password-reset/done/', views.password_reset_done, name='password_reset_done'),
    path('reset/<uidb64>/<token>/', 
         views.CustomPasswordResetConfirmView.as_view(), 
         name='password_reset_confirm'),
    path('reset/done/', 
         auth_views.PasswordResetCompleteView.as_view(template_name='password_reset_complete.html'),
         name='password_reset_complete'),
    path('todo/', views.todo_view, name='todo'),
    path('api/todos/', views.TodoViewSet.as_view({'get': 'list', 'post': 'create'}), name='todo-list'),
    path('api/todos/<int:pk>/', views.TodoViewSet.as_view({
        'get': 'retrieve',
        'patch': 'partial_update',
        'delete': 'destroy'
    }), name='todo-detail'),
] + router.urls  # Add the router URLs
