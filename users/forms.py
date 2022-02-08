"""users form."""
from django import forms
#Models
from django.contrib.auth.models import User
from users.models import Profile

#Validamos los campos de creacion de cuenta
class SignupForm(forms.Form):
    """Sign up form."""
    username = forms.CharField(
        min_length=4,
        max_length=50,
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Username',
                'class': 'form-control',
                'required': True
                }
        )
    )
    password = forms.CharField(
        min_length=6,
        max_length=70,
        widget=forms.PasswordInput(
            attrs={
                'placeholder': 'Password',
                'class': 'form-control',
                'required': True
            }
        )
    )
    password_confirmation = forms.CharField(
        min_length=6,
        max_length=70,
        widget = forms.PasswordInput(
            attrs={
                'placeholder': 'Password Confirmation',
                'class': 'form-control',
                'required': True
            }
        )
    )

    first_name = forms.CharField(
        min_length=3,
        max_length=50,
        widget=forms.TextInput(
            attrs={
                'placeholder':'First name',
                'class': 'form-control',
                'required': True
            }
        )
    )
    last_name = forms.CharField(
        min_length=3,
        max_length=50,
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Last name',
                'class': 'form-control',
                'required': True
            }
        )
    )

    email = forms.CharField(
        min_length=6,
        max_length=70,
        widget=forms.EmailInput(
            attrs={
                "placeholder": "email",
                "class": "form-control",
                'required': True
            }
        )
    )

#Clase para verificar que el usuario existe y debe de crear otro
    def clean_username(self):
        """username must be unique"""
        username= self.cleaned_data['username']
        username_taken = User.objects.filter(username=username).exists()
        if username_taken:
            raise forms.ValidationError('username is already use.!')
        return username
#verificacion del password que sea el mismo que de confirmacion
    def clean(self):

        """verify password confirmation match"""
        data = super().clean()
        password= data['password']
        password_confirmation= data['password_confirmation']
        if password != password_confirmation:
            raise forms.ValidationError('Password dos not match')
        return data

    def save(self):
        data = self.cleaned_data
        data.pop('password_confirmation')
        user = User.objects.create_user(**data)
        profile = Profile(user=user)
        profile.save()


class ProfileForm(forms.Form):
    """Profile form."""
    website = forms.URLField(max_length=200, required=True)
    biography = forms.CharField(max_length=200, required=False)
    phone_number = forms.CharField(max_length=20, required=False)
    picture = forms.ImageField(required=False)