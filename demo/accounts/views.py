from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm
from .forms import CustomUserCreationForm
from django.contrib.auth.decorators import login_required
from .models import ModProfile
from django import forms


def register(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Auto-login after registration
            return redirect('todo')  # Redirect to user's To-Do list
    else:
        form = CustomUserCreationForm()
    
    return render(request, "register.html", {"form": form})


def login_view(request):
    if request.method == "POST":
        form = LoginForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('todo')
    else:
        form = LoginForm()
    
    return render(request, "login.html", {"form": form})

def logout_view(request):
    logout(request)
    return redirect('login')  # Redirect to login after logout

@login_required
def toggle_theme(request):
    if request.user.is_mod:
        mod_profile, created = ModProfile.objects.get_or_create(user=request.user)
        mod_profile.theme = "dark" if mod_profile.theme == "light" else "light"
        mod_profile.save()
    return redirect("todo")

class LoginForm(forms.Form):  # or whatever form you're using
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500'
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500'
        })
    )
