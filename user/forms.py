from django import forms
from django.forms import ModelForm 
from django.contrib.auth.forms import UserCreationForm
from .models import *

class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class DatingProfileForm(forms.ModelForm):
    class Meta:
        model = DatingProfile
        fields = ['gender', 'age', 'bio', 'location', 'interests']


class LoginForm(forms.Form):
    username = forms.CharField(max_length=100)
    password = forms.CharField(widget=forms.PasswordInput)


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = DatingProfile
        fields = ['profile_picture']