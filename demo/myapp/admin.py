from django.contrib import admin
from myapp.models import TodoItem  # Instead of Todo

# Register your models here.
admin.site.register(TodoItem)