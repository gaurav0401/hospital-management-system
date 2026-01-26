from django import forms
from django.core.exceptions import ValidationError
from .models import User
import re

class DoctorSignupForm(forms.ModelForm):
    password1 = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = [
            'username', 'first_name', 'last_name',
            'email', 'contact', 'gender',
            'specialty', 'years_of_experience'
        ]

    def clean_password1(self):
        pwd = self.cleaned_data.get('password1')
        if len(pwd) < 8:
            raise ValidationError("Password must be at least 8 characters.")
        if not re.search(r'[A-Z]', pwd):
            raise ValidationError("Password must contain one uppercase letter.")
        if not re.search(r'\d', pwd):
            raise ValidationError("Password must contain one number.")
        return pwd

    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data.get('password1') != cleaned_data.get('password2'):
            raise ValidationError("Passwords do not match.")
        return cleaned_data
    def clean_email(self):
        email = self.cleaned_data.get('email')

        if User.objects.filter(email=email).exists():
            raise ValidationError(
                "This email is already registered. Please use a different email."
            )

        return email
    def clean_username(self):
        username = self.cleaned_data.get('username')

        if User.objects.filter(username=username).exists():
            raise ValidationError(
                "This username is already taken. Please choose another one."
            )

        return username




class PatientSignupForm(forms.ModelForm):
    password1 = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(widget=forms.PasswordInput)


    class Meta:
        model = User
        fields = [
            'username', 'first_name', 'last_name',
            'email', 'contact', 'gender',
            'date_of_birth'
        ]
        widgets = {
            'date_of_birth': forms.DateInput(
                attrs={
                    'type': 'date',          
                    'class': 'form-control'
                }
            )
        }

    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data.get('password1') != cleaned_data.get('password2'):
            raise ValidationError("Passwords do not match.")
        return cleaned_data
    def clean_email(self):
        email = self.cleaned_data.get('email')

        if User.objects.filter(email=email).exists():
            raise ValidationError(
                "This email is already registered. Please use a different email."
            )

        return email
    def clean_username(self):
        username = self.cleaned_data.get('username')

        if User.objects.filter(username=username).exists():
            raise ValidationError(
                "This username is already taken. Please choose another one."
            )

        return username
