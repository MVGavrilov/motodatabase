from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


class LoginForm(forms.Form):

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)

    username = forms.CharField(label='Username', max_length=100)
    password = forms.CharField(label='Password', widget=forms.PasswordInput)

    def get_user(self):  # TODO: добавить логин по e-mail
        user = User.objects.filter(username=self.clean_username()).first()
        return user

    def clean_username(self):
        username = self.cleaned_data['username']
        user = User.objects.filter(username=username).first()
        if not user:
            raise ValidationError('You entered an invalid username.')
        return username

    def clean_password(self):
        password = self.cleaned_data['password']
        if 'username' in self.cleaned_data:
            user = self.get_user()
            if not user.check_password(password):
                raise ValidationError('You entered an invalid password.')
        return password

    @property
    def field_order(self):
        return ['username', 'password']
