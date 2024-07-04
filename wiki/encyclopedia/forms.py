from django import forms
from .models import Entry, Tag
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class EntryForm(forms.ModelForm):
    tag = forms.ModelMultipleChoiceField(
        queryset=Tag.objects.all(),
        required=False,
        widget=forms.CheckboxSelectMultiple
    )

    class Meta:
        model = Entry
        fields = ['title', 'content', 'image', 'bio_content', 'category', 'tag', 'reference']
        widgets = {
            'category': forms.Select,  # Use Select widget for category
        }

class EditEntryForm(forms.ModelForm):
    tag = forms.ModelMultipleChoiceField(
        queryset=Tag.objects.all(),
        required=False,
        widget=forms.CheckboxSelectMultiple
    )

    class Meta:
        model = Entry
        fields = ['content', 'image', 'bio_content', 'category', 'tag', 'reference']
        widgets = {
            'category': forms.Select,  # Use Select widget for category
        }
class UserRegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email']

        