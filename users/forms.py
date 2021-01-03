from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password1', 'password2']

    def clean(self):
        super().clean()
        email = self.cleaned_data.get('email')
       
        if User.objects.filter(email=email).exists():
            raise ValidationError("Email already exists")
       
        return self.cleaned_data
