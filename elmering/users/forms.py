from django import forms
from users.models import CustomUser
from django.contrib.auth.forms import (
    AuthenticationForm,
    UserCreationForm,
    UserChangeForm,
    PasswordChangeForm
    )


class UserRegistrationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = (
            'email',
            'password1',
            'password2',
        )


class UserLoginForm(AuthenticationForm):
    username = forms.EmailField(
        label='Email',
        widget=forms.EmailInput(attrs={'autofocus': True}),
    )

    def __init__(self, request=None, *args, **kwargs):
        super().__init__(request, *args, **kwargs)
        self.fields['username'].label = "Email"
        self.fields['password'].label = "Password"


class UserProfileForm(UserChangeForm):
    class Meta:
        model = CustomUser
        # fields = "__all__"
        fields = ['username']


class UserPasswordChangeForm(PasswordChangeForm):
    class Meta:
        model = CustomUser
