from django import forms
from ..models import Task


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'function_name', 'function_starter', 'description', 'max_attempts', 'end_date']
