from django import forms


class PlaygroundForm(forms.Form):
    code = forms.CharField(label='Function Code', widget=forms.Textarea, required=True)
    args = forms.CharField(label='Arguments', required=False, widget=forms.TextInput(
        attrs={'class': 'w-full border border-gray-300 rounded-md py-2 px-3 focus:outline-none focus:border-blue-500'}))
    expected = forms.CharField(label='Expected Output', required=False, widget=forms.TextInput(
        attrs={'class': 'w-full border border-gray-300 rounded-md py-2 px-3 focus:outline-none focus:border-blue-500'}))
    function = forms.CharField(label='Function Name', max_length=100, required=True, widget=forms.TextInput(
        attrs={'class': 'w-full border border-gray-300 rounded-md py-2 px-3 focus:outline-none focus:border-blue-500'}))
