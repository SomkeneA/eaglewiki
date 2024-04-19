from django import forms

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class EntryForm(forms.Form):
    title = forms.CharField(label="Title", max_length=100)
    content = forms.CharField(label="Content", widget=forms.Textarea)
class EditEntryForm(forms.Form):
    content = forms.CharField(label="Content", widget=forms.Textarea)

class UserRegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email']