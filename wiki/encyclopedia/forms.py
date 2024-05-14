from django import forms
from .models import Entry
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class EntryForm(forms.Form):
    title = forms.CharField(label="Title", max_length=100)
    content = forms.CharField(label="Content", widget=forms.Textarea)
    image = forms.ImageField(label="Image", required=False)
    category = forms.CharField(label="Category", max_length=100, required=False)
    tag = forms.CharField(label="Tag", max_length=100, required=False)
    reference = forms.CharField(label="Reference", max_length=255, required=False)

class EditEntryForm(forms.ModelForm):
    class Meta:
        model = Entry
        fields = ['content', 'image', 'category', 'tag', 'reference']


class UserRegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email']