from django.shortcuts import render, redirect
from .models import TodoItem
from .forms import TodoForm
from django.contrib.auth.decorators import login_required
from django.conf import settings

def home(request):
    return render(request, "home.html")

@login_required  # Ensures only logged-in users can see their to-do list
def todo(request):
    todos = TodoItem.objects.filter(user=request.user)
    context = {
        'todos': todos,
        'mapbox_token': settings.MAPBOX_ACCESS_TOKEN
    }
    return render(request, 'todo.html', context)

@login_required
def add_todo(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        location_name = request.POST.get('location_name')
        latitude = request.POST.get('latitude')
        longitude = request.POST.get('longitude')
        
        if title:
            TodoItem.objects.create(
                title=title,
                description=description,
                user=request.user,
                location_name=location_name,
                latitude=latitude if latitude else None,
                longitude=longitude if longitude else None
            )
    return redirect('todo')

@login_required
def toggle_todo(request, todo_id):
    todo = TodoItem.objects.get(id=todo_id, user=request.user)
    todo.completed = not todo.completed
    todo.save()
    return redirect('todo')

@login_required
def delete_todo(request, todo_id):
    todo = TodoItem.objects.get(id=todo_id, user=request.user)
    todo.delete()
    return redirect('todo')
