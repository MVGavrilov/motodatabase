from django import forms
from django.contrib.auth.hashers import check_password
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError

from assortment.models import Manufacturer


class LoginForm(forms.Form):

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)  # TODO: разобраться, что за хрень
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
            raise ValidationError('Пользователя с таким логином не существует.')
        return username

    def clean_password(self):
        password = self.cleaned_data['password']
        if 'username' in self.cleaned_data:
            user = self.get_user()
            if not user.check_password(password):
                raise ValidationError('Неправильный пароль.')
        return password

    @property
    def field_order(self):
        return ['username', 'password']


class AddManufacturerForm(forms.Form):
    name = forms.CharField(label='Name', max_length=100)

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('instance', None)  # TODO: разобраться, что за хрень
        super().__init__(*args, **kwargs)

    def clean_name(self):
        name = self.cleaned_data['name']
        if Manufacturer.objects.filter(name=name).first():
            raise ValidationError(name + ' был добавлен ранее.')
        return name


class AddUserForm(forms.Form):
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('instance', None)  # TODO: разобраться, что за хрень
        super().__init__(*args, **kwargs)

    username = forms.CharField(label='Username', max_length=100)
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    email = forms.EmailField(label='Email', max_length=100)
    first_name = forms.CharField(label='First name', max_length=100)
    last_name = forms.CharField(label='Last name', max_length=100)
    is_staff = forms.BooleanField(label='Is staff', required=False)

    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).first():
            raise ValidationError('Пользователя с таким логином уже существует.')
        return username

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).first():
            raise ValidationError('Пользователя с таким e-mail уже существует.')
        return email

    def clean_password(self):
        password = self.cleaned_data['password']
        if validate_password(password):
            raise ValidationError('Пароль не удовлетворяет требованиям.')
        return password