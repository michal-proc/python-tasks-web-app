from django import forms


class JoinGroupAsStudentForm(forms.Form):
    join_code_student = forms.CharField(max_length=40, required=True, label="Join Code for Student")
