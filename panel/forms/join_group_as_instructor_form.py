from django import forms


class JoinGroupAsInstructorForm(forms.Form):
    join_code_instructor = forms.CharField(max_length=40, required=True, label="Join Code for Instructor")
