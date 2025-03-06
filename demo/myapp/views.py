from django.shortcuts import render, redirect
from .models import TodoItem
from .forms import TodoForm
from django.contrib.auth.decorators import login_required

def home(request):
    return render(request, "home.html")

@login_required  # Ensures only logged-in users can see their to-do list
def todo(request):
    todos = TodoItem.objects.filter(user=request.user)  # Show only user's tasks
    form = TodoForm()

    if request.method == 'POST':
        form = TodoForm(request.POST)
        if form.is_valid():
            todo = form.save(commit=False)
            todo.user = request.user  # Assign the task to the logged-in user
            todo.save()
            return redirect('todo')  # Redirect to prevent form resubmission

    return render(request, 'todo.html', {'todos': todos, 'form': form})
