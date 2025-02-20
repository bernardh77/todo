from django import forms
from myapp.models import TodoItem  # Instead of Todo

class TodoForm(forms.ModelForm):
    class Meta:
        model = TodoItem
        fields = ['title']  # Only allow the user to add a title
