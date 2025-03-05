from django.contrib import admin
from .models import CustomUser, Todo  # Import your custom user model and Todo model

admin.site.register(CustomUser)
admin.site.register(Todo)
