from django import forms
from .models import Feedback,CustomUser,Location
from django.contrib.auth.forms import UserCreationForm
class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ['rating', 'comment']

class LocationForm(forms.ModelForm):
    class Meta:
        model = Location
        fields = ['url']

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'password1', 'password2', 'mobile_number', 'address']