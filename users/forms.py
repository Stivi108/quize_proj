from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Profile, User

class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('teamLead',)
