from django import forms
from ..models import Solution


class SolutionForm(forms.ModelForm):
    solution_type = forms.ChoiceField(choices=[('file', 'File'), ('text', 'Text')], widget=forms.RadioSelect)
    python_code = forms.CharField(widget=forms.Textarea, required=False)

    class Meta:
        model = Solution
        fields = ['task', 'solution_file', 'user']
