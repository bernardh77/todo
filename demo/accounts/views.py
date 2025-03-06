from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm
from .forms import CustomUserCreationForm
from django.contrib.auth.decorators import login_required
from .models import ModProfile
from django import forms
from django.core.mail import send_mail, BadHeaderError
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.models import User
from django.template.loader import render_to_string
from django.db.models.query_utils import Q
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.http import HttpResponse
from django.contrib.auth import get_user_model
import logging  # Add this import
from django.contrib.auth.views import PasswordResetConfirmView
from django.urls import reverse_lazy

logger = logging.getLogger(__name__)

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

def password_reset_request(request):
    User = get_user_model()
    if request.method == "POST":
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            logger.info(f"Processing password reset for email: {email}")  # Debug log
            users = User.objects.filter(Q(email=email))
            if users.exists():
                for user in users:
                    subject = "Password Reset Requested"
                    email_template_name = "registration/password_reset_email.txt"
                    context = {
                        "email": user.email,
                        'domain': request.META['HTTP_HOST'],
                        'site_name': 'Your Site',
                        "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                        "user": user,
                        'token': default_token_generator.make_token(user),
                        'protocol': 'https' if request.is_secure() else 'http',
                    }
                    email_message = render_to_string(email_template_name, context)
                    try:
                        logger.info("Attempting to send email")  # Debug log
                        send_mail(
                            subject,
                            email_message,
                            "todo123789@gmail.com",
                            [user.email],
                            fail_silently=False,
                        )
                        logger.info("Email sent successfully")  # Debug log
                    except Exception as e:
                        logger.error(f"Failed to send email: {str(e)}")  # Debug log
                        return HttpResponse(f'Error sending email: {str(e)}')
                    return redirect("password_reset_done")
            else:
                logger.warning(f"No user found with email: {email}")  # Debug log
    else:
        form = PasswordResetForm()
    return render(request, "password_reset.html", {"form": form})

def password_reset_done(request):
    return render(request, "password_reset_done.html")

class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'password_reset_confirm.html'
    success_url = reverse_lazy('password_reset_complete')
    
    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        # Add Tailwind CSS classes to form fields
        for field in form.fields.values():
            field.widget.attrs.update({
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500'
            })
        return form

def password_reset_complete(request):
    return render(request, "password_reset_complete.html")
