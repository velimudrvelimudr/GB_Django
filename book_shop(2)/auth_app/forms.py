from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserChangeForm, UserCreationForm
from django.db.models import fields
from .models import BookUser
from auth_app import models
from random import random
from hashlib import sha1


class BookLoginUserForm(AuthenticationForm):
    class Meta:
        model = BookUser
        fields = ('username', 'password')

    def __init__(self, *args, **kwargs):
        super(BookLoginUserForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'


class BookUserEditForm(UserChangeForm):
    class Meta:
        model = BookUser
        fields = ['username', 'email', 'password', 'first_name', 'last_name', 'age', 'avatar']


    def  __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            field.help_text = ''
            if field_name == 'password':
                field.widget = forms.HiddenInput()


class BookUserRegisterForm(UserCreationForm):
    class Meta:
        model = BookUser
        fields = ['username', 'email', 'password1', 'password2', 'first_name', 'last_name', 'age', 'avatar']


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            field.help_text = ''

    def save(self):
        user = super(BookUserRegisterForm, self).save()
        user.is_active = False
        salt = sha1(str(random()).encode('utf-8')).hexdigest()[:6]
        user.activation_key = sha1((user.email + salt).encode('utf_8')).hexdigest()
        user.save()

        return user

