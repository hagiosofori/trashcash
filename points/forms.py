from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

from .models import Client, Trash_Submission


class SignUpForm(UserCreationForm):
    phone_number = forms.CharField(
        required=True,
        max_length=10, 
        help_text="Required. Please enter a Ghanaian phone number",
    )

    class Meta:
        model = User
        fields = [
            'username',
            'phone_number',
            'password1',
            'password2',
        ]
    

class TrashSubmissionForm(forms.ModelForm):
    class Meta:
        model = Trash_Submission
        fields = [
            'user',
            'weight',
        ]

class NewSuperUserForm(forms.ModelForm):
    class Meta:
        model = User
        exclude = [
            'last_login', 
            'user_permissions',
            'groups',
            'date_joined',
            'is_active',
        ]