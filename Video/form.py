from django import forms

class NameForm(forms.Form):
    name=forms.CharField(label="Entrez le nom", max_length=50)
    message = forms.CharField(widget=forms.Textarea)
    sender = forms.EmailField()